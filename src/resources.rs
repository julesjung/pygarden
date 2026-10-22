use macroquad::audio::{Sound, load_sound_from_bytes};
use macroquad::miniquad::conf::Icon;
use macroquad::prelude::*;

pub const ICON: Icon = Icon {
    small: *include_bytes!("../assets/icon16.rgba"),
    medium: *include_bytes!("../assets/icon32.rgba"),
    big: *include_bytes!("../assets/icon64.rgba"),
};

pub struct Assets {
    pub logo: Texture2D,
    pub placements: [Texture2D; 3],
    pub plant_textures: [Texture2D; 12],
    pub font: Font,
    pub music: [Sound; 4],
    pub background: Texture2D,
}

impl Assets {
    pub async fn load() -> Self {
        let logo = Texture2D::from_file_with_format(include_bytes!("../assets/logo.png"), None);

        clear_background(BLACK);
        draw_texture(&logo, 256.0, 280.0, WHITE);
        next_frame().await;

        let placements = [
            Texture2D::from_file_with_format(
                include_bytes!("../assets/placements/plains.png"),
                None,
            ),
            Texture2D::from_file_with_format(
                include_bytes!("../assets/placements/water.png"),
                None,
            ),
            Texture2D::from_file_with_format(
                include_bytes!("../assets/placements/savannah.png"),
                None,
            ),
        ];

        let plant_textures = [
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/oak.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/sakura.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/birch.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/pine.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/clovers.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/kelp.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/nenuphar.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/corals.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/acacia.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/cactus.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/palm.png"), None),
            Texture2D::from_file_with_format(include_bytes!("../assets/plants/baobab.png"), None),
        ];

        for texture in plant_textures.iter() {
            texture.set_filter(FilterMode::Nearest);
        }

        let font = load_ttf_font_from_bytes(include_bytes!("../assets/fonts/dohyeon-regular.ttf"))
            .unwrap();

        let music = [
            load_sound_from_bytes(include_bytes!("../assets/music/soundtrack_1.ogg"))
                .await
                .unwrap(),
            load_sound_from_bytes(include_bytes!("../assets/music/soundtrack_2.ogg"))
                .await
                .unwrap(),
            load_sound_from_bytes(include_bytes!("../assets/music/soundtrack_3.ogg"))
                .await
                .unwrap(),
            load_sound_from_bytes(include_bytes!("../assets/music/soundtrack_4.ogg"))
                .await
                .unwrap(),
        ];

        let background =
            Texture2D::from_file_with_format(include_bytes!("../assets/background.png"), None);

        Assets {
            logo,
            placements,
            plant_textures,
            font,
            music,
            background,
        }
    }
}
