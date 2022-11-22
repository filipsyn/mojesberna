FROM python:alpine

# Stage for copying only requirements.txt file
#
# This file is copied by itself and not with the rest of the source code
# due to the caching mechanism in Docker (each step is cached, so if there were no changes to requirements.txt, there is
# no need to copy and install it)
COPY src/requirements.txt src/
RUN pip install --no-cache-dir --upgrade -r src/requirements.txt

# Copying source files into container
COPY src/ /src/

# Setting envrionmental variables needed to run the application
ENV FLASK_APP='src/app.py'
ENV FLASK_DEBUG=1

# Running flask local server
#
# --port flag specifies that application will be listening on port :80
#
# --host flag specifies that application will be hosted at wildcard address 0.0.0.0
# 	That means the app will be accessible not only from localhost address but also from address in local network.
#	Accessibility from local network is useful for testing application on mobile devices.

CMD ["flask", "run", "--port", "80", "--host", "0.0.0.0"]