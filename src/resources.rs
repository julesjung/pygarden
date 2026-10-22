use macroquad::audio::{Sound, load_sound_from_bytes};
use macroquad::miniquad::conf::Icon;
use macroquad::prelude::*;

pub const ICON: Icon = Icon {
    small: *include_bytes!("../assets/icon16.rgba"),
    medium: *include_bytes!("../assets/icon32.rgba"),
    big: *include_bytes!("../assets/icon64.rgba"),
};

pub struct Assets {
    pub background: Texture2D,
    pub placements: [Texture2D; 3],
    pub plant_textures: [Texture2D; 12],
    pub music: [Sound; 4],
}

impl Assets {
    pub async fn load() -> Self {
        let logo = Texture2D::from_file_with_format(include_bytes!("../assets/logo.png"), None);

        let mut progress = 0;
        let total = 21;

        macro_rules! load {
            (texture2d $s:literal) => {{
                let texture = Texture2D::from_file_with_format(include_bytes!($s), None);
                texture.set_filter(FilterMode::Nearest);
                progress += 1;

                clear_background(BLACK);
                draw_texture(&logo, 256.0, 280.0, WHITE);
                draw_bar(256.0, 504.0, 512.0, 32.0, progress as f32 / total as f32);
                next_frame().await;

                texture
            }};

            (sound $s:literal) => {{
                let sound = load_sound_from_bytes(include_bytes!($s)).await.unwrap();
                progress += 1;

                clear_background(BLACK);
                draw_texture(&logo, 256.0, 280.0, WHITE);
                draw_bar(256.0, 504.0, 512.0, 32.0, progress as f32 / total as f32);
                next_frame().await;

                sound
            }};

            (font $s:literal) => {{
                let font = load_ttf_font_from_bytes(include_bytes!($s)).unwrap();
                progress += 1;

                clear_background(BLACK);
                draw_texture(&logo, 256.0, 280.0, WHITE);
                draw_bar(256.0, 504.0, 512.0, 32.0, progress as f32 / total as f32);
                next_frame().await;

                font
            }};
        }

        clear_background(BLACK);
        draw_texture(&logo, 256.0, 280.0, WHITE);
        next_frame().await;

        let background = load!(texture2d "../assets/background.png");

        let placements = [
            load!(texture2d "../assets/placements/plains.png"),
            load!(texture2d "../assets/placements/water.png"),
            load!(texture2d "../assets/placements/savannah.png"),
        ];

        let plant_textures = [
            load!(texture2d "../assets/plants/oak.png"),
            load!(texture2d "../assets/plants/sakura.png"),
            load!(texture2d "../assets/plants/birch.png"),
            load!(texture2d "../assets/plants/pine.png"),
            load!(texture2d "../assets/plants/clovers.png"),
            load!(texture2d "../assets/plants/kelp.png"),
            load!(texture2d "../assets/plants/nenuphar.png"),
            load!(texture2d "../assets/plants/corals.png"),
            load!(texture2d "../assets/plants/acacia.png"),
            load!(texture2d "../assets/plants/cactus.png"),
            load!(texture2d "../assets/plants/palm.png"),
            load!(texture2d "../assets/plants/baobab.png"),
        ];

        let font = load!(font "../assets/fonts/dohyeon-regular.ttf");

        let music = [
            load!(sound "../assets/music/soundtrack_1.ogg"),
            load!(sound "../assets/music/soundtrack_2.ogg"),
            load!(sound "../assets/music/soundtrack_3.ogg"),
            load!(sound "../assets/music/soundtrack_4.ogg"),
        ];

        Assets {
            placements,
            plant_textures,
            music,
            background,
        }
    }
}

fn draw_bar(x: f32, y: f32, w: f32, h: f32, t: f32) {
    draw_rectangle(
        x,
        y,
        w * t.clamp(0.0, 1.0),
        h,
        Color::from_rgba(61, 110, 112, 255),
    );
    draw_rectangle_lines(x, y, w, h, 2.0, WHITE);
}
