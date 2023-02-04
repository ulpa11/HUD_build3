from django.core.exceptions import ValidationError

#validator to check music file
def validate_audio_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3', '.wav', '.aac']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

#validator to check music file
def validate_photo_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".jpg", ".jpeg",".png"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')