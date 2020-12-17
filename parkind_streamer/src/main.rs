extern crate opencv;

use opencv::{
    core,
    highgui,
    prelude::*,
    videoio,
};
use clap::Clap;

#[derive(Clap)]
#[clap(version = "0.0.1", author = "Kornel Domeradzki <korneldomeradzki1@gmail.com>")]
struct Opts {
    /// path to the configuration file
    #[clap(short, long)]
    config: String,
    /// enables local image preprocessing
    #[clap(short, long, default=false)]
    preprocessing: bool,
    /// enables connection requests from sources unspecified in config file
    #[clap(short, long, default=false)]
    allow_untrusted: bool,
}

fn run() -> opencv::Result<()> {
    let window = "video capture";
    highgui::named_window(window, 1)?;
    #[cfg(feature = "opencv-32")]
    let mut cam = videoio::VideoCapture::new_default(0)?;  // 0 is the default camera
    #[cfg(not(feature = "opencv-32"))]
    let mut cam = videoio::VideoCapture::new(0, videoio::CAP_ANY)?;  // 0 is the default camera
    let opened = videoio::VideoCapture::is_opened(&cam)?;
    if !opened {
        panic!("Unable to open default camera!");
    }
    loop {
        let mut frame = core::Mat::default()?;
        cam.read(&mut frame)?;
        if frame.size()?.width > 0 {
            highgui::imshow(window, &mut frame)?;
        }
        let key = highgui::wait_key(10)?;
        if key > 0 && key != 255 {
            break;
        }
    }
    Ok(())
}

fn main() {
    let opts: Opts = Opts::parse();
    run().unwrap()
}