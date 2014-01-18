ART      = 'art-default.jpg'
ICON     = 'icon-default.png'
BASEURL = 'http://cdn.media.ccc.de/congress/'

def Start():
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = '30C3'
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime = 300

@handler('/video/30c3', '30C3', art=ART, thumb=ICON) 
def MainMenu():

	oc = ObjectContainer(no_cache=True)

	oc.add(DirectoryObject(
		key = Callback(GetIdentifiers, title="30c3"),
		title = "30C3"
		))
	
	oc.add(DirectoryObject(
		key = Callback(GetIdentifiers, title="29c3"),
		title = "29C3"
		))

	return oc

#############################################################################################################

@route('/video/30c3/identifiers')
def GetIdentifiers(title):

	summary = 'Summary'
	
	oc = ObjectContainer()
	
	if title == '30c3':
		VIDEO_LIST_URL = BASEURL + '2013/mp4/'
	elif title == '29c3':
		VIDEO_LIST_URL = BASEURL + '2012/mp4-h264-HQ/'

		
	for url in HTML.ElementFromURL(VIDEO_LIST_URL).xpath('//a[contains(@href, ".mp4")]/@href'):
		title = url.split('-de-')[-1].split('-en-')[-1].split('_h264')[0].replace('_', ' ')

		oc.add(CreateVideoClipObject(
			url = '%s%s' % (VIDEO_LIST_URL, url),
			title = title
		))

	return oc

#############################################################################################################
@route('/video/cccde/createvideoclipobject', include_container=bool)
def CreateVideoClipObject(url, title, include_container=False):

	videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoClipObject, url=url, title=title, include_container=True),
		rating_key = url,
		title = title,
		summary = 'summary',
		items = [
			MediaObject(
				parts = [
					PartObject(key=url)
				],
				container = Container.MP4,
				video_codec = VideoCodec.H264,
				video_resolution = '720',
				audio_codec = AudioCodec.AAC,
				audio_channels = 2,
				optimized_for_streaming = True
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj
