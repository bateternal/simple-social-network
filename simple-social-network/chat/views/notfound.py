from django.http import HttpResponse


def notfound(request):
    return HttpResponse(
        """<html>
                <style>
                    body {
                        background-image: url('/media/AsahNlC0VhQ');
                        background-position: center;
                        background-repeat: no-repeat;
                        background-size: cover;
                        margin: 0;
                        height: 100%;
                    }
                </style>
                <body>
                </body>
            </html>
        """
        )
