This is a **Django-based API** for managing contents, channels, and groups. The project allows users to upload files, manage channels and their contents, filter channels by groups, and calculate content ratings.

## Features

- Manage Contents, Channels, and Groups
- Upload and validate file types for contents (e.g., videos, videos, pdfs, or text)
- Rating system for contents with validation (0-10 range)
- Filter channels by associated groups
- Dockerized for easy setup and deployment

## Model Design and Validation

The project involves several Django models like `Channel`, `Content`, `File`, and `Group`, each serving distinct purposes:

**File Model & Validation**

* **File Upload** : The `File` model allows for file uploads, and each file is associated with content (`ForeignKey` relation). The `FileField` allows you to store files, and a custom `FileExtensionValidator` ensures that only files with certain extensions are allowed (e.g., `.MOV`, `.mp4`, `.pdf`, `.docx`).
* **Validation** : The `FileExtensionValidator` checks the file type upon upload. It prevents invalid files from being uploaded, protecting the system from handling unexpected or unsupported file formats.

**Content Model & Rating Validation**

* The `Content` model holds details about individual pieces of content, including a `rating` field with a value between `0` and `10`.
* The `clean()` method performs custom validation to ensure that the rating stays within the valid range. This validation ensures that invalid content cannot be saved in the database.

## Channel Model and Conditional Relations

The `Channel` model has a more complex structure, allowing for relationships with:

* **Contents** : A channel can include multiple pieces of content (`ManyToManyField`).
* **Subchannels** : A channel can have subchannels in a self-referential `ManyToManyField`.

**Clean Method for Channel Validation**

* The custom `clean()` method ensures that a `Channel` can either have `contents` or `subchannels`, but not both at the same time.

**Average Rating Calculation**

* The `avg_rating()` method calculates the average rating for a channel, considering either its subchannels or its contents. If a channel has subchannels, it aggregates the ratings of those subchannels. If it only has content, it averages the content ratings.

## API Design Using DRF

**Serializers**

* **ContentSerializer** : Handles serialization and deserialization of `Content` instances. During creation and updating, it supports nested file data, allowing for files to be associated with content on the fly.
* **ChannelSerializer** : Serializes `Channel` data, supporting nested relationships like `contents` and `subchannels`. It also ensures that the response includes the average rating calculation if necessary.
* **GroupSerializer** : Manages the serialization of `Group` objects, primarily used for filtering channels by group.

**Custom Create and Update Methods**

* In the `ContentSerializer`, custom `create` and `update` methods are implemented to handle the relationship between `Content` and `File`. For example, when content is created or updated, associated file data is either created or updated accordingly. This ensures that related data (like files) is properly handled when working with content.

## Filtering Channels by Group

**Channel Filtering**

* The `ChannelListView` supports filtering channels by their associated groups. This is implemented using the `DjangoFilterBackend` and allows you to filter channels based on the group id or group name using query parameters.
* Example:
  * `/channels/?groups__id=1`: This returns all channels associated with `group1`
  * `/channels/?groups__name=group1`: This returns all channels associated with `group1`.

**Custom List Method for Response Formatting**

* In the `ChannelListView`, the `list()` method is overridden to format the response. If no data is found during a request, it returns a `204 No Content` status instead of the usual `200 OK`. This improves API clarity by signaling when no results are available for a particular query.

## File Validation and Handling

**File Validation**

* The `FileExtensionValidator` is applied to the `file` field in the `File` model, which ensures that only allowed file types (e.g., `.mp4`, `.pdf`, `.txt`) can be uploaded.

## Dockerization

**Docker Setup**

* **Dockerfile** : Defines the environment in which the Django app runs, ensuring a consistent setup across different environments. It includes all necessary dependencies, such as `Python`, `Django`, and `PostgreSQL`.
* **Docker Compose** : The `docker-compose.yml` file defines two services:
* **Web** : The Django app.
* **Database** : PostgreSQL service used by the app.

  This setup allows the project to be run using a single command (`docker-compose up --build`), making it easy to set up for development or deployment without worrying about local dependencies or environment differences.

## Unit Testing

Tests were implemented to ensure that key functionalities are working as expected:

* **Channels and content**: Ensuring correct behavior in managing and retrieving channels and their contents.
* **Content Rating Validation**: Tests check that the rating system enforces the `0-10` range.
* **File uploads**:Tests ensure that only allowed file types can be uploaded, and invalid files are rejected.
* **Channel Filtering by Group**: Tests verify that channels can be successfully filtered by their associated group.
* **Rating validation**: Ensuring the rating system adheres to the 0–10 range.

These tests are crucial for maintaining the integrity of the app and preventing bugs when new features are introduced.

## Management Command

A custom **Django management command** was created to efficiently calculate the ratings of every channel and export them in a csv file sorted by rating..

## Technologies

- **Backend**: Python, Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Others**: Django Filter, Python typing, File validation, Custom management commands

## Project Structure

![1727830854046](image/README/1727830854046.png)

## Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.10+**
- **PostgreSQL**
- **Docker & Docker Compose** (if you plan to use Docker)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/wajibola/media_platform.git
   cd media_platform
   ```
2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   venv\Scripts\activate source venv/bin/activate  # On Linux use source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Set up PostgreSQL and update settings.py:**

   ```bash
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }

   # Static files (CSS, JavaScript, Images)
   # https://docs.djangoproject.com/en/5.1/howto/static-files/

   STATIC_URL = 'static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'static')
   MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
   MEDIA_URL = '/media/
   ```
4. **Run migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. **Build and run the services using Docker Compose:**

   ```bash
   docker-compose up --build
   ```
2. **Run migrations inside the docker container (in another terminal):**

   ```bash
   docker-compose exec web python manage.py migrate
   ```

### Available Endpoints

Here are the main endpoints exposed by the API:

* **Content Endpoints** :

  * `GET /api/contents/`: List all contents
  * `GET /api/contents/<id>/`: Retrieve a specific content
* **Channel Endpoints** :

  * `GET /api/channels/`: List all channels (with filtering by group)
  * `GET /api/channels/<id>/`: Retrieve a specific channel
* **Group Endpoints** :

  * `GET /api/groups/`: List all groups
  * `GET /groups/<id>/`: Retrieve a specific group
* **Filtering** :

  * `GET /api/channels/?groups__id=<group_id>`: Filter channels by group id
  * `GET /api//channels/?groups__name=<group_name>`: Filter channels by group name

### Running Tests

To run the unit tests for the project:

1. **Without Docker** :

   ```bash
   python manage.py test
   ```
2. **With Docker** :

   ```bash
   docker-compose exec web python manage.py test
   ```

### Management Commands

A management command was created to efficiently calculate the ratings of every channel and export them in a csv file sorted by rating.

```bash
python manage.py export_channel_ratings
```
