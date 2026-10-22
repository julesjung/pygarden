use std::path::Path;
use std::process::Command;
use std::{env, fs};

fn main() {
    compress_music();
}

fn compress_music() {
    let src = Path::new("assets/music");
    let out = Path::new(&env::var("OUT_DIR").unwrap()).join("music");
    fs::create_dir_all(&out).unwrap();
    println!("cargo:rerun-if-changed=assets/music");

    for entry in fs::read_dir(src).unwrap() {
        let path = entry.unwrap().path();
        if path.extension().and_then(|e| e.to_str()) != Some("wav") {
            continue;
        }
        let dest = out.join(path.file_stem().unwrap()).with_extension("ogg");

        let status = Command::new("ffmpeg")
            .args(["-y", "-v", "error", "-i"])
            .arg(&path)
            .args(["-c:a", "libvorbis", "-q:a", "4", "-ar", "44100"])
            .arg(&dest)
            .status()
            .expect("ffmpeg not found: install ffmpeg with libvorbis support");

        assert!(status.success(), "ffmpeg failed on {}", path.display());
    }
}
