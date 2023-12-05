from django.http.response import FileResponse, HttpResponseNotFound

import lyceum.settings

__all__ = []


def download(request, path):
    file_path = lyceum.settings.MEDIA_ROOT / path
    file = file_path.name
    try:
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f"attachment; filename={file}"
        return response
    except FileNotFoundError:
        return HttpResponseNotFound()
