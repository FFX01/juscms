# juscms
juscms is a simple cms for generating a static website. Pages can be added through the django admin(enhanced with grapelli). juscms is currently in a pre-alpha stat and is not ready for deployment.

## Functionality
- Create static pages with normal html content through a row and chunk interface.
- Modify page header and footer through HTML
- Hierarchical page structure managed by django-mptt
- set any page as the 'home' page
- juscms does not make any assumptions about page structure or styling. The end user is able to define how 'rows' and 'chunks' behave through their own css.
- extensible by subclassing the base 'Page' model or the 'HTMLContent' model

## Goals
- Simplify creation of more content types
- Add more extensive testing
- mixin classes for defining new content types
- Better separation of concerns through decoupling templates from their models
- Allowing third party 'themes'
- More intuitive admin functionality
- more robust 'Footer' and 'Header' models
- Allow media file management and uploading through admin. Also allow media files to be added to models easily.

