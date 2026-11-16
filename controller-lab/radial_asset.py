"""Create the original circular UI plate; no stock game art is copied."""
import math
import struct

RESOURCE = 'PSTPRAD'
SELECTION_RESOURCE = 'PSTPSEL'
SIZE = 420

def build_radial_bam():
    # BAM V1: one uncompressed indexed frame, transparent green at index zero.
    palette = [(0, 255, 0), (23, 20, 17), (99, 81, 65)]
    palette_bytes = b''.join(bytes((b, g, r, 0)) for r, g, b in palette)
    palette_bytes += bytes((256 - len(palette)) * 4)
    pixels = bytearray(SIZE * SIZE)
    center = (SIZE - 1) / 2
    for y in range(SIZE):
        for x in range(SIZE):
            radius = math.hypot(x - center, y - center)
            pixels[y * SIZE + x] = 0 if radius > 209.5 else 2 if radius >= 207.5 else 1
    frame_offset, palette_offset, lookup_offset = 24, 40, 1064
    data_offset = lookup_offset + 2
    header = b'BAM V1  ' + struct.pack('<HBBIII', 1, 1, 0, frame_offset, palette_offset, lookup_offset)
    frame = struct.pack('<HHhhI', SIZE, SIZE, 0, 0, data_offset | 0x80000000)
    cycle = struct.pack('<HH', 1, 0)
    return header + frame + cycle + palette_bytes + struct.pack('<H', 0) + pixels

def build_selection_bam():
    """Sidebar and action highlight frames (yellow), plus a white ring sight.

    Frame 0: 64x64 yellow square frame (sidebar).
    Frame 1: 57x97 yellow tall frame (action buttons).
    Frame 2: 48x48 WHITE ring - the freecam sights, drawn like the game's own
    selected-character circle: 2px-thick, opaque white, transparent center.
    """
    import math
    palette=bytes((0,255,0,0, 8,10,12,0, 64,221,255,0, 255,255,255,255))+bytes(252*4)
    sizes=[(64,64),(57,97),(48,48)]
    frame_offset=24
    palette_offset=frame_offset+len(sizes)*12+len(sizes)*4
    lookup_offset=palette_offset+1024
    data_offset=lookup_offset+len(sizes)*2
    frames=[]; images=[]
    for index,(width,height) in enumerate(sizes):
        pixels=bytearray(width*height)
        if index<2:
            for y in range(height):
                for x in range(width):
                    edge=min(x,y,width-1-x,height-1-y)
                    pixels[y*width+x]=1 if edge==0 else 2 if edge in (1,2) else 0
        else:
            cx=cy=(width-1)/2
            radius=width/2-2
            for y in range(height):
                for x in range(width):
                    d=math.sqrt((x-cx)**2+(y-cy)**2)
                    # Anti-aliased-ish 2px ring: solid white core with a
                    # soft edge pixel at each boundary.
                    if radius-1.2 <= d <= radius+1.2:
                        pixels[y*width+x]=3
                    elif radius-2.2 <= d < radius-1.2 or radius+1.2 < d <= radius+2.2:
                        pixels[y*width+x]=3
        frames.append(struct.pack('<HHhhI',width,height,0,0,data_offset|0x80000000))
        images.append(bytes(pixels)); data_offset+=len(pixels)
    return (b'BAM V1  '+struct.pack('<HBBIII',3,3,0,frame_offset,palette_offset,lookup_offset)
            +b''.join(frames)+b''.join(struct.pack('<HH',1,i) for i in range(3))
            +palette+struct.pack('<3H',0,1,2)+b''.join(images))

def build_ui_assets():
    return {RESOURCE+'.bam':build_radial_bam(),SELECTION_RESOURCE+'.bam':build_selection_bam()}
