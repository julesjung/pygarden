use bevy::prelude::*;

use crate::camera::{MainCamera, cursor_world_position};

#[derive(Component)]
pub struct Shop;

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
        Transform::from_xyz(528.0, 448.0, 0.0),
        Shop,
    ));
}

pub fn open_shop(
    mut commands: Commands,
    mouse: Res<ButtonInput<MouseButton>>,
    window: Single<&Window>,
    camera: Single<(&Camera, &GlobalTransform), With<MainCamera>>,
    shop: Single<(&Transform, &Sprite), With<Shop>>,
    assets: Res<Assets<Image>>,
    asset_server: Res<AssetServer>,
) {
    if mouse.just_pressed(MouseButton::Left) {
        let Some(world_position) = cursor_world_position(window, camera) else {
            return;
        };

        let (shop_transform, shop_sprite) = shop.into_inner();

        let image_size = assets.get(&shop_sprite.image).unwrap().size_f32();

        let bounding_box =
            Rect::from_center_size(shop_transform.translation.truncate(), image_size);

        if bounding_box.min.x < world_position.x
            && bounding_box.min.y < world_position.y
            && bounding_box.max.x > world_position.x
            && bounding_box.max.y > world_position.y
        {
            commands.spawn((
                AudioPlayer(asset_server.load::<AudioSource>("sounds/door_opening.wav")),
                PlaybackSettings {
                    mode: bevy::audio::PlaybackMode::Despawn,
                    ..Default::default()
                },
            ));
        }
    }
}
