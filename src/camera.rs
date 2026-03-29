use bevy::{camera::ScalingMode, prelude::*};

#[derive(Component)]
pub struct MainCamera;

pub fn setup_camera(mut commands: Commands) {
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

pub fn move_camera(
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

pub fn cursor_world_position(
    window: Single<&Window>,
    camera: Single<(&Camera, &GlobalTransform), With<MainCamera>>,
) -> Option<Vec2> {
    let (camera, camera_transform) = camera.into_inner();
    let cursor_position = window.cursor_position()?;

    camera
        .viewport_to_world_2d(camera_transform, cursor_position)
        .ok()
}
