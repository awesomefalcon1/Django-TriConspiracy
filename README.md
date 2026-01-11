## Blog

A simple Django blog application with Materialize CSS UI. Features include blog posts, categories, tags, and a clean, modern interface.

### Features

- **Blog Posts**: Create, view, and manage blog posts
- **Categories**: Organize posts by categories
- **Tags**: Tag posts for better organization
- **Publishing**: Draft/publish workflow for posts
- **Modern UI**: Materialize CSS design
- **Tor Hidden Service**: Configured to run as a Tor hidden service

### Models

- **BlogPost**: Main blog post model with title, content, excerpt, author, category, tags, and publishing status
- **Category**: Categories for organizing posts
- **Tag**: Tags for labeling posts

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

4. Run the server:
```bash
python manage.py runserver
```

### Usage

- Visit `/` to see all published blog posts
- Visit `/create/` to create a new blog post
- Visit `/admin/` to manage posts, categories, and tags via Django admin
- Posts can be filtered by category or tag
- Only published posts are visible to visitors

### Tor Hidden Service

This blog is configured to run as a Tor hidden service. See `TOR_SETUP_INSTRUCTIONS.md` for setup details.
