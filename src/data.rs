use serde::{Deserialize, Serialize};

use crate::plant::Plant;

#[derive(Default, Deserialize, Serialize)]
pub struct Data {
    pub plants: [[Option<Plant>; 8]; 3],
}

impl Data {
    pub fn load() -> Self {
        let data = std::fs::read("game.json").unwrap_or_default();

        serde_json::from_slice(&data).unwrap_or_default()
    }

    pub fn save(&self) -> std::io::Result<()> {
        let data = serde_json::to_vec(self).unwrap();

        std::fs::write("game.json", data)
    }
}
