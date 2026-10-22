use macroquad::prelude::*;
use serde::{Deserialize, Serialize};

use crate::resources::Assets;

const PLANT_WIDTH: f32 = 192.0;
const PLANT_HEIGHT: f32 = 256.0;

#[repr(usize)]
#[derive(Debug, Clone, Copy, Deserialize, Serialize)]
pub enum PlantKind {
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
#[derive(Debug, Clone, Copy, Deserialize, Serialize)]
enum Growth {
    Sprout = 0,
    NoLeaves = 1,
    FullyGrown = 2,
}

#[derive(Deserialize, Serialize)]
pub struct Plant {
    kind: PlantKind,
    growth: Growth,
}

impl Plant {
    pub fn new(kind: PlantKind) -> Plant {
        Plant {
            kind,
            growth: Growth::Sprout,
        }
    }

    pub fn grow(&mut self) {
        self.growth = match self.growth {
            Growth::Sprout => Growth::NoLeaves,
            Growth::NoLeaves => Growth::FullyGrown,
            Growth::FullyGrown => Growth::FullyGrown,
        };
    }

    pub fn draw(&self, assets: &Assets, x: f32, y: f32) {
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
