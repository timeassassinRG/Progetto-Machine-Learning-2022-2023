#import bing downloader
from bing_image_downloader import downloader
downloader.download("Pianoforte", limit=200,  output_dir='Piano_bing', adult_filter_off=True, force_replace=False, timeout=120)