name_to_dxf_code = {
    'type': 0, # Text string indicating the entity type (fixed)
    'object': 0, # Text string indicating the entity type (fixed)
    'objectname': 0, # Text string indicating the entity type (fixed)
    'text': 1, # Primary text value for an entity
    'name': 2, # Name (attribute tag, block name, and so on)
    'handle': 5, # "Entity handle; text string of up to 16 hexadecimal digits (fixed)"
    'linetype': 6, # Linetype name (fixed)
    'text_style': 7, # Text style name (fixed)
    'textstyle': 7, # Text style name (fixed)
    'layer': 8, # Layer name (fixed)
    'layer_name': 8, # Layer name (fixed)
    'center': 10, # "Primary point; this is the start point of a line or text entity, center of a circle, and so on"
    'insertionpoint': 10, # "Primary point; this is the start point of a line or text entity, center of a circle, and so on"
    'startpoint': 10, # "Primary point; this is the start point of a line or text entity, center of a circle, and so on"
    'position': 10, # "Primary point; this is the start point of a line or text entity, center of a circle, and so on"

    'center_x': 11,
    'insertionpoint_x': 11,
    'startpoint_x': 11,
    'position_x': 11,

    'center_y': 21,
    'insertionpoint_y': 21,
    'startpoint_y': 21,
    'position_y': 21,

    'center_z': 31,
    'insertionpoint_z': 31,
    'startpoint_z': 31,
    'position_z': 31,

    'unit_direction': 11,
    'endpoint': 21,
    'end_point': 21,
    'thikness': 39, # Entity's thickness if nonzero (fixed)
    'radius': 40, # Floatingtopoint values (text height, scale factors, and so on) to48
    'text_height': 40, # Floatingtopoint values (text height, scale factors, and so on) to48
    'width': 40, # Floatingtopoint values (text height, scale factors, and so on) to48
    'xscale': 41,
    'xscale_factor': 41,
    'rect_width': 41,
    'height': 41,
    'yscale': 42,
    'yscale_factor': 42,
    'zscale': 43,
    'zscale_factor': 43,
    'linetype_scale': 48, # "Linetype scale; floatingtopoint scalar value; default value is defined for all entity types"
    'line_scale lyne_type_scale': 48, # "Linetype scale; floatingtopoint scalar value; default value is defined for all entity types"
    'rotation': 50, # Angles (output in degrees to DXF files and radians through AutoLISP and ObjectARX applications) to58
    'angle': 50, # Angles (output in degrees to DXF files and radians through AutoLISP and ObjectARX applications) to58
    'visibility': 60, # "Entity visibility; integer value; absence or 0 indicates visibility; 1 indicates invisibility"
    'color': 62, # Color number (fixed)
    'color_number': 62, # Color number (fixed)
    'is_paper_space': 67, # Spacetothat is, model or paper space (fixed)
    'column_count': 70, # Integer values, such as repeat counts, flag bits, or modesto78
    'flags': 70, # Integer values, such as repeat counts, flag bits, or modesto78
    'ole_version': 70, # Integer values, such as repeat counts, flag bits, or modesto78
    'extrusion': 210, # Extrusion direction (fixed)
    'extrusion_direction': 210, # Extrusion direction (fixed)
}