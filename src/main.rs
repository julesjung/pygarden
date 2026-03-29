mod camera;
mod game;
mod loading;
mod soundtrack;

use crate::camera::{move_camera, setup_camera};
use crate::game::{open_shop, setup_game};
use crate::loading::{despawn_logo, fade_in_logo, setup_loading_screen};
use crate::soundtrack::{setup_soundtrack, update_soundtrack};
use bevy::prelude::*;
use bevy::window::EnabledButtons;

#[derive(States, Default, Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum GameState {
    #[default]
    Loading,
    InGame,
}

fn main() -> AppExit {
    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: String::from("PyGarden"),
                resolution: (1024, 768).into(),
                resizable: false,
                enabled_buttons: EnabledButtons {
                    maximize: false,
                    ..Default::default()
                },
                ..Default::default()
            }),
            ..Default::default()
        }))
        .init_state::<GameState>()
        .add_systems(Startup, setup_camera)
        .add_systems(OnEnter(GameState::Loading), setup_loading_screen)
        .add_systems(OnExit(GameState::Loading), despawn_logo)
        .add_systems(OnEnter(GameState::InGame), (setup_game, setup_soundtrack))
        .add_systems(Update, fade_in_logo.run_if(in_state(GameState::Loading)))
        .add_systems(
            Update,
            (move_camera, update_soundtrack, open_shop).run_if(in_state(GameState::InGame)),
        )
        .run()
}
