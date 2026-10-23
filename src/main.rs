#![windows_subsystem = "windows"]

mod audio;
mod data;
mod plant;
mod resources;

use macroquad::prelude::*;
use macroquad::ui::{hash, root_ui, widgets};

use crate::audio::MusicPlayer;
use crate::data::Data;
use crate::plant::Plant;
use crate::resources::{Assets, ICON};

const PLANT_POSITIONS: [Vec2; 8] = [
    vec2(128.0, 64.0),
    vec2(320.0, 64.0),
    vec2(512.0, 64.0),
    vec2(704.0, 64.0),
    vec2(128.0, 320.0),
    vec2(320.0, 320.0),
    vec2(512.0, 320.0),
    vec2(704.0, 320.0),
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
    let mut hovered_plant: Option<usize> = None;
    let mut selected_plant: Option<usize> = None;
    let mut selected_biome = 0usize;
    let mut selected_plant_types: (usize, usize, usize) = (0, 0, 0);

    let plant_window_id = hash!();

    let assets = Assets::load().await;

    let mut data = Data::load();

    let mut music_player = MusicPlayer::new();

    loop {
        draw_background(&assets, selected_biome);

        for (index, (position, plant)) in PLANT_POSITIONS
            .iter()
            .zip(data.plants[selected_biome].iter())
            .enumerate()
        {
            let hovered = Some(index) == hovered_plant;

            match plant {
                Some(plant) => plant.draw(&assets, position.x, position.y, hovered),
                None => draw_placement(&assets, selected_biome, position.x, position.y, hovered),
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

                    ui.tree_node(hash!(), "Caméra", |ui| {
                        ui.combo_box(
                            hash!(),
                            "Biome",
                            &["Plaine", "Mer", "Savanne"],
                            &mut selected_biome,
                        );
                    });
                });
        }

        if let Some(index) = selected_plant {
            let window_position = PLANT_POSITIONS[index] + vec2(0.0, 256.0);

            root_ui().window(plant_window_id, window_position, vec2(256.0, 128.0), |ui| {
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

                    data.plants[selected_biome][index] = Some(Plant::new(kind))
                }

                if let Some(plant) = &mut data.plants[selected_biome][index] {
                    if ui.button(None, "Faire pousser") {
                        plant.grow();
                    }
                }
            });
        }

        music_player.update();

        hovered_plant = None;
        let position = mouse_position();

        if !root_ui().is_mouse_captured() && !root_ui().is_mouse_over(vec2(position.0, position.1))
        {
            for (index, plant_position) in PLANT_POSITIONS.iter().enumerate() {
                if is_in_bounding_box(plant_position, position.0, position.1) {
                    hovered_plant = Some(index);
                    break;
                }
            }

            if is_key_pressed(KeyCode::F1) {
                editor = !editor;
            }

            if is_mouse_button_pressed(MouseButton::Left) {
                if selected_plant != hovered_plant {
                    selected_plant = hovered_plant;

                    if let Some(selected) = selected_plant {
                        let window_position = PLANT_POSITIONS[selected] + vec2(0.0, 256.0);

                        root_ui().move_window(plant_window_id, window_position);
                    }
                }
            }
        }

        next_frame().await
    }
}

fn is_in_bounding_box(plant_position: &Vec2, x: f32, y: f32) -> bool {
    let plant_right = plant_position.x;
    let plant_top = plant_position.y;
    let plant_left = plant_right + 192.0;
    let plant_bottom = plant_top + 256.0;

    plant_right < x && x < plant_left && plant_top < y && y < plant_bottom
}

fn draw_placement(assets: &Assets, biome: usize, x: f32, y: f32, hovered: bool) {
    let texture = &assets.placements[biome];

    let color = match hovered {
        false => WHITE,
        true => Color::from_rgba(255, 200, 200, 255),
    };

    draw_texture(&texture, x, y, color);
}
