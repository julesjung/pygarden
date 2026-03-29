use bevy::{audio::PlaybackMode, prelude::*};
use rand::{prelude::*, rng};

#[derive(Resource)]
pub struct SoundtrackPlayer {
    track_list: Vec<Handle<AudioSource>>,
    current_index: usize,
}

#[derive(Component)]
pub struct Soundtrack;

impl SoundtrackPlayer {
    fn new(track_list: Vec<Handle<AudioSource>>) -> Self {
        Self {
            track_list,
            current_index: 0,
        }
    }

    fn next(&mut self) -> Handle<AudioSource> {
        self.current_index = (self.current_index + 1) % self.track_list.len();

        self.track_list[self.current_index].clone()
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

    let soundtrack = SoundtrackPlayer::new(track_list);

    commands.spawn((
        AudioPlayer(soundtrack.track_list[soundtrack.current_index].clone()),
        PlaybackSettings {
            mode: PlaybackMode::Despawn,
            ..Default::default()
        },
        Soundtrack,
    ));

    commands.insert_resource(soundtrack);
}

pub fn update_soundtrack(
    mut commands: Commands,
    query: Query<(), With<Soundtrack>>,
    mut soundtrack: ResMut<SoundtrackPlayer>,
) {
    if query.is_empty() {
        let entity = commands.spawn((
            AudioPlayer(soundtrack.next()),
            PlaybackSettings {
                mode: PlaybackMode::Despawn,
                ..Default::default()
            },
            Soundtrack,
        ));
    }
}
