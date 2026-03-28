use bevy::prelude::*;

use crate::GameState;

#[derive(Component)]
pub struct Logo;

pub fn setup_loading_screen(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        Sprite {
            image: asset_server.load("logo.png"),
            color: Srgba::new(1.0, 1.0, 1.0, 0.0).into(),
            ..Default::default()
        },
        Transform::default(),
        Logo,
    ));
}

pub fn fade_in_logo(
    mut commands: Commands,
    time: Res<Time>,
    mut query: Query<&mut Sprite, With<Logo>>,
) {
    let Ok(mut logo) = query.single_mut() else {
        return;
    };

    let elapsed = time.elapsed_secs();

    logo.color.set_alpha((elapsed / 2.0).clamp(0.0, 1.0));

    if elapsed >= 2.0 {
        commands.set_state(GameState::InGame);
    }
}
