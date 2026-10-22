#![windows_subsystem = "windows"]

mod audio;
mod data;
mod plant;
mod resources;

use std::io::Cursor;

use kira::sound::streaming::StreamingSoundData;
use kira::{AudioManager, AudioManagerSettings, DefaultBackend};
use macroquad::prelude::*;
use macroquad::ui::{hash, root_ui, widgets};

use crate::audio::MusicPlayer;
use crate::data::Data;
use crate::plant::Plant;
use crate::resources::{Assets, ICON};

const PLANT_POSITIONS: [(f32, f32); 8] = [
    (128.0, 64.0),
    (320.0, 64.0),
    (512.0, 64.0),
    (704.0, 64.0),
    (128.0, 320.0),
    (320.0, 320.0),
    (512.0, 320.0),
    (704.0, 320.0),
];

fn window_conf() -> Conf {
    Conf {
        window_title: String::from("PyGarden"),
        window_width: 1024,
        window_height: 768,
        high_dpi: false,
        fullscreen: false,
        window_resizable: false,
        icon: Some(ICON),
        ..Default::default()
    }
}

fn draw_background(assets: &Assets, biome: usize) {
    clear_background(BLACK);

    let (x, y) = match biome {
        0 => (0.0, 0.0),
        1 => (0.0, 768.0),
        2 => (1024.0, 768.0),
        _ => (0.0, 0.0),
    };

    draw_texture_ex(
        &assets.background,
        0.0,
        0.0,
        WHITE,
        DrawTextureParams {
            source: Some(Rect::new(x, y, 1024.0, 768.0)),
            ..Default::default()
        },
    );
}

#[macroquad::main(window_conf)]
async fn main() {
    clear_background(BLACK);
    next_frame().await;

    let mut editor = false;
    let mut selected_biome = 0usize;
    let mut selected_plant_types: (usize, usize, usize) = (0, 0, 0);

    let assets = Assets::load().await;

    let mut data = Data::load();

    let mut music_player = MusicPlayer::new();

    loop {
        draw_background(&assets, selected_biome);

        for (position, plant) in PLANT_POSITIONS
            .iter()
            .zip(data.plants[selected_biome].iter())
        {
            match plant {
                Some(plant) => plant.draw(&assets, position.0, position.1),
                None => draw_placement(&assets, selected_biome, position.0, position.1),
            };
        }

        if editor {
            widgets::Window::new(hash!(), vec2(768.0, 0.0), vec2(256.0, 512.0))
                .label("BABOAB")
                .titlebar(true)
                .ui(&mut *root_ui(), |ui| {
                    if ui.button(None, "Charger") {
                        data = Data::load();
                    }
                    if ui.button(None, "Enregistrer") {
                        data.save().unwrap();
                    }

                    ui.tree_node(hash!(), "Planter", |ui| {
                        match selected_biome {
                            0 => {
                                ui.combo_box(
                                    hash!(),
                                    "Type",
                                    &["Chêne", "Cerisier du Japon", "Bouleau", "Sapin"],
                                    &mut selected_plant_types.0,
                                );
                            }
                            1 => {
                                ui.combo_box(
                                    hash!(),
                                    "Type",
                                    &["Trèfles", "Algues", "Nénuphar", "Coraux"],
                                    &mut selected_plant_types.1,
                                );
                            }
                            2 => {
                                ui.combo_box(
                                    hash!(),
                                    "Type",
                                    &["Acacia", "Cactus", "Palmier", "Baobab"],
                                    &mut selected_plant_types.2,
                                );
                            }
                            _ => (),
                        };
                        if ui.button(None, "Planter") {
                            let kind = unsafe {
                                std::mem::transmute(match selected_biome {
                                    0 => selected_plant_types.0,
                                    1 => 4 + selected_plant_types.1,
                                    2 => 8 + selected_plant_types.2,
                                    _ => 0,
                                })
                            };
                            data.plants[selected_biome][0] = Some(Plant::new(kind))
                        }

                        if ui.button(None, "Faire pousser") {
                            match &mut data.plants[selected_biome][0] {
                                Some(plant) => plant.grow(),
                                None => (),
                            }
                        }
                    });

                    ui.tree_node(hash!(), "Caméra", |ui| {
                        ui.combo_box(
                            hash!(),
                            "Biome",
                            &["Plaine", "Mer", "Savanne"],
                            &mut selected_biome,
                        );
                    });

                    ui.tree_node(hash!(), "Musique", |ui| {});
                });
        }

        if is_key_pressed(KeyCode::F1) {
            editor = !editor;
        }

        music_player.update();

        next_frame().await
    }
}

fn draw_placement(assets: &Assets, biome: usize, x: f32, y: f32) {
    let texture = &assets.placements[biome];

    draw_texture(&texture, x, y, WHITE);
}
