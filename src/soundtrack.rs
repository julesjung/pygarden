use bevy::{audio::PlaybackMode, prelude::*};
use rand::{prelude::*, rng};

#[derive(Resource)]
pub struct SoundtrackPlayer {
    track_list: Vec<Handle<AudioSource>>,
    current: usize,
}

impl SoundtrackPlayer {
    fn new(track_list: Vec<Handle<AudioSource>>) -> Self {
        Self {
            track_list,
            current: 0,
        }
    }

    fn next(&mut self) -> Handle<AudioSource> {
        self.current = (self.current + 1) % self.track_list.len();

        self.track_list[self.current].clone()
    }
}

pub fn setup_soundtrack(mut commands: Commands, asset_server: Res<AssetServer>) {
    let mut track_list = vec![
        asset_server.load("music/soundtrack_1.mp3"),
        asset_server.load("music/soundtrack_2.mp3"),
        asset_server.load("music/soundtrack_3.mp3"),
        asset_server.load("music/soundtrack_4.mp3"),
    ];

    track_list.shuffle(&mut rng());

    commands.insert_resource(SoundtrackPlayer::new(track_list));
}

pub fn update_soundtrack(
    mut commands: Commands,
    query: Query<Entity, With<AudioSink>>,
    mut soundtrack: ResMut<SoundtrackPlayer>,
) {
    if query.is_empty() {
        commands.spawn((
            AudioPlayer(soundtrack.next()),
            PlaybackSettings {
                mode: PlaybackMode::Once,
                ..Default::default()
            },
        ));
    }
}
