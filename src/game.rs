use bevy::prelude::*;

pub fn setup_game(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        Sprite {
            image: asset_server.load("background.png"),
            ..Default::default()
        },
        Transform::from_xyz(0.0, 0.0, -1.0),
    ));

    commands.spawn((
        Sprite {
            image: asset_server.load("shop.png"),
            ..Default::default()
        },
        Transform::from_xyz(1552.0, 1216.0, 0.0),
    ));
}
