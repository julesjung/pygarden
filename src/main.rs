mod loading;
mod soundtrack;

use crate::loading::{fade_in_logo, setup_loading_screen};
use crate::soundtrack::{setup_soundtrack, update_soundtrack};
use bevy::camera::ScalingMode;
use bevy::prelude::*;
use bevy::window::EnabledButtons;

#[derive(States, Default, Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum GameState {
    #[default]
    Loading,
    InGame,
}

#[derive(Component)]
struct MainCamera;

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
        .add_systems(Startup, setup)
        .add_systems(OnEnter(GameState::Loading), setup_loading_screen)
        .add_systems(OnEnter(GameState::InGame), (setup_game, setup_soundtrack))
        .add_systems(Update, fade_in_logo.run_if(in_state(GameState::Loading)))
        .add_systems(
            Update,
            (move_camera, update_soundtrack).run_if(in_state(GameState::InGame)),
        )
        .run()
}

fn setup(mut commands: Commands) {
    commands.spawn((
        Camera2d,
        Projection::Orthographic(OrthographicProjection {
            scaling_mode: ScalingMode::Fixed {
                width: 1024.0,
                height: 768.0,
            },
            ..OrthographicProjection::default_2d()
        }),
        MainCamera,
    ));
}

fn setup_game(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        Sprite {
            image: asset_server.load("background.png"),
            ..Default::default()
        },
        Transform::from_xyz(0.0, 0.0, 0.0),
    ));
}

fn move_camera(
    buttons: Res<ButtonInput<MouseButton>>,
    windows: Query<&Window>,
    mut camera: Query<&mut Transform, With<MainCamera>>,
    mut last_cursor: Local<Option<Vec2>>,
) {
    let Ok(window) = windows.single() else {
        return;
    };

    let Some(cursor) = window.cursor_position() else {
        *last_cursor = None;
        return;
    };

    if buttons.pressed(MouseButton::Left) {
        if let Some(prev) = *last_cursor {
            let delta = cursor - prev;

            let Ok(mut transform) = camera.single_mut() else {
                return;
            };

            transform.translation.x = (transform.translation.x - delta.x).clamp(-512.0, 512.0);
            transform.translation.y = (transform.translation.y + delta.y).clamp(-384.0, 384.0);
        }
    } else {
        *last_cursor = None;
    }

    *last_cursor = Some(cursor);
}
