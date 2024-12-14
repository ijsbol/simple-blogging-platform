# A (very) simple blogging platform

## Self hosting
1. Make a copy of `sample.blog-authors.json` and rename to `blog-authors.json`
2. Check out `blogs/sample.example.mdx`
    - Public blogs follow the naming format of `blog.slug-here.mdx`
    - Private blogs follow the naming format of `private.slug-here.mdx`
    - i.e. replace `sample.` with `blog.` for public and `private.` for private blogs
3. Create a python venv (`python -m venv venv`)
4. Activate is (`source venv/bin/activate`)
5. Install requirements (`pip install -r requirements.txt`)
6. Run with `uvicorn router:app`

