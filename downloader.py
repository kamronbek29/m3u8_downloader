import asyncio
import json
from uuid import uuid4

import aiohttp
import m3u8


FILE_DIRECTORY = 'downloads/'


async def get_hls_info(m3u8_url):
    hls_info = m3u8.load(m3u8_url, verify_ssl=False)
    hls_info_data = json.dumps(hls_info.data)
    hls_info_json = json.loads(hls_info_data)
    base_url = hls_info.base_uri

    return hls_info_json, base_url


async def download_file(hls_url, file_type):
    hls_info, base_url = await get_hls_info(hls_url)
    list_segments = hls_info['segments']

    file_directory = '{0}/{1}.{2}'.format(FILE_DIRECTORY, uuid4(), file_type)
    with open(file_directory, 'wb') as file_to_write:
        async with aiohttp.ClientSession() as session:
            for downloaded, one_segment in enumerate(list_segments, start=1):
                part_uri = one_segment['uri']
                full_url = f'{base_url}/{part_uri}'

                get_video = await session.get(full_url, ssl=False)
                video_url_content = await get_video.content.read()
                file_to_write.write(video_url_content)

    return file_directory


if __name__ == '__main__':
    asyncio.run(download_file('', 'mp3'))
