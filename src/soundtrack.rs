use bevy::{audio::PlaybackMode, prelude::*};
use rand::{prelude::*, rng};

#[derive(Resource)]
pub struct SoundtrackPlayer {
    track_list: Vec<Handle<AudioSource>>,
    current_index: usize,
    current_entity: Option<Entity>,
}

impl SoundtrackPlayer {
    fn new(track_list: Vec<Handle<AudioSource>>) -> Self {
        Self {
            track_list,
            current_index: 0,
            current_entity: None,
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

    let mut soundtrack = SoundtrackPlayer::new(track_list);

    let entity = commands.spawn((
        AudioPlayer(soundtrack.track_list[soundtrack.current_index].clone()),
        PlaybackSettings {
            mode: PlaybackMode::Despawn,
            ..Default::default()
        },
    ));
    soundtrack.current_entity = Some(entity.id());

    commands.insert_resource(soundtrack);
}

pub fn update_soundtrack(
    mut commands: Commands,
    query: Query<(), With<AudioPlayer>>,
    mut soundtrack: ResMut<SoundtrackPlayer>,
) {
    if let Some(current_entity) = soundtrack.current_entity
        && query.get(current_entity).is_err()
    {
        let entity = commands.spawn((
            AudioPlayer(soundtrack.next()),
            PlaybackSettings {
                mode: PlaybackMode::Despawn,
                ..Default::default()
            },
        ));
        soundtrack.current_entity = Some(entity.id());
    }
}
