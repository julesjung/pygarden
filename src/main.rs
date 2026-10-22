#![windows_subsystem = "windows"]

mod resources;

use macroquad::audio::{PlaySoundParams, play_sound};
use macroquad::prelude::*;
use macroquad::rand::rand;
use macroquad::ui::{hash, root_ui, widgets};

use crate::resources::{Assets, ICON};

const PLANT_WIDTH: f32 = 192.0;
const PLANT_HEIGHT: f32 = 256.0;

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

    let mut selected_biome = 0usize;
    let mut selected_plant_types: (usize, usize, usize) = (0, 0, 0);

    let assets = Assets::load().await;

    play_sound(
        &assets.music[(rand() as usize) % 4],
        PlaySoundParams {
            looped: true,
            volume: 1.0,
        },
    );

    let mut plants: [[Option<Plant>; 8]; 3] = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ];

    loop {
        draw_background(&assets, selected_biome);

        for (position, plant) in PLANT_POSITIONS.iter().zip(plants[selected_biome].iter()) {
            match plant {
                Some(plant) => plant.draw(&assets, position.0, position.1),
                None => draw_placement(&assets, selected_biome, position.0, position.1),
            };
        }

        widgets::Window::new(hash!(), vec2(0.0, 0.0), vec2(192.0, 128.0))
            .label("Camera")
            .titlebar(true)
            .ui(&mut *root_ui(), |ui| {
                ui.combo_box(
                    hash!(),
                    "Biome",
                    &["Plaine", "Mer", "Savanne"],
                    &mut selected_biome,
                );
            });

        widgets::Window::new(hash!(), vec2(768.0, 0.0), vec2(256.0, 512.0))
            .label("Gestion des données")
            .titlebar(true)
            .close_button(true)
            .ui(&mut *root_ui(), |ui| {
                ui.group(hash!(), vec2(256.0, 256.0), |ui| {
                    ui.label(None, "Nouvel arbre");
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
                        plants[selected_biome][0] = Some(Plant::new(kind))
                    }
                });

                ui.group(hash!(), vec2(256.0, 256.0), |ui| {
                    if ui.button(None, "Faire pousser") {
                        match &mut plants[selected_biome][0] {
                            Some(plant) => plant.grow(),
                            None => (),
                        }
                    }
                });
            });

        next_frame().await
    }
}

#[repr(usize)]
#[derive(Debug, Clone, Copy)]
enum PlantKind {
    Oak = 0,
    Sakura = 1,
    Birch = 2,
    Pine = 3,
    Clovers = 4,
    Kelp = 5,
    Nenuphar = 6,
    Corals = 7,
    Acacia = 8,
    Cactus = 9,
    Palm = 10,
    Baobab = 11,
}

#[repr(usize)]
#[derive(Debug, Clone, Copy)]
enum Growth {
    Sprout = 0,
    NoLeaves = 1,
    FullyGrown = 2,
}

struct Plant {
    kind: PlantKind,
    growth: Growth,
}

impl Plant {
    fn new(kind: PlantKind) -> Plant {
        Plant {
            kind,
            growth: Growth::Sprout,
        }
    }
}

impl Plant {
    fn grow(&mut self) {
        self.growth = match self.growth {
            Growth::Sprout => Growth::NoLeaves,
            Growth::NoLeaves => Growth::FullyGrown,
            Growth::FullyGrown => Growth::FullyGrown,
        };
    }

    fn draw(&self, assets: &Assets, x: f32, y: f32) {
        let texture = assets.plant_textures.get(self.kind as usize).unwrap();

        draw_texture_ex(
            &texture,
            x,
            y,
            WHITE,
            DrawTextureParams {
                source: Some(Rect::new(
                    PLANT_WIDTH * (self.growth as usize) as f32,
                    0.0,
                    PLANT_WIDTH,
                    PLANT_HEIGHT,
                )),
                ..Default::default()
            },
        );
    }
}

fn draw_placement(assets: &Assets, biome: usize, x: f32, y: f32) {
    let texture = &assets.placements[biome];

    draw_texture(&texture, x, y, WHITE);
}
