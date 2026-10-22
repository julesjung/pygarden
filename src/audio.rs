use std::io::Cursor;

use fastrand::shuffle;
use kira::sound::streaming::{StreamingSoundData, StreamingSoundHandle};
use kira::sound::{FromFileError, PlaybackState};
use kira::{AudioManager, AudioManagerSettings, DefaultBackend};

pub struct MusicPlayer {
    playlist: [&'static [u8]; 5],
    current_song: usize,
    manager: AudioManager,
    handle: StreamingSoundHandle<FromFileError>,
}

impl MusicPlayer {
    pub fn new() -> Self {
        let mut playlist: [&[u8]; _] = [
            include_bytes!(concat!(
                env!("OUT_DIR"),
                "/music/les_feuilles_mortes_racontent_une_histoire.ogg"
            )),
            include_bytes!(concat!(
                env!("OUT_DIR"),
                "/music/sommes_nous_suffisament_vivants.ogg"
            )),
            include_bytes!(concat!(
                env!("OUT_DIR"),
                "/music/la_brise_dun_printemps_lointain.ogg"
            )),
            include_bytes!(concat!(
                env!("OUT_DIR"),
                "/music/par_dela_lhorizon_qui_nous_separe.ogg"
            )),
            include_bytes!(concat!(env!("OUT_DIR"), "/music/bonus.ogg")),
        ];

        shuffle(&mut playlist);

        let mut manager =
            AudioManager::<DefaultBackend>::new(AudioManagerSettings::default()).unwrap();
        let music = StreamingSoundData::from_cursor(Cursor::new(playlist[0])).unwrap();

        let handle = manager.play(music).unwrap();

        MusicPlayer {
            playlist,
            current_song: 0,
            manager,
            handle,
        }
    }

    pub fn update(&mut self) {
        if self.handle.state() == PlaybackState::Stopped {
            self.next_song();
        }
    }

    fn next_song(&mut self) {
        self.current_song += 1;
        self.current_song %= self.playlist.len();

        let music =
            StreamingSoundData::from_cursor(Cursor::new(self.playlist[self.current_song])).unwrap();

        self.handle = self.manager.play(music).unwrap();
    }
}
