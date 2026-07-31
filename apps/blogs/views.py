from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from .models import Blog, BlogCategory, Tag, Comment

try:
    import markdown
except ImportError:
    markdown = None

class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)
        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')
        query = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
            )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Blog.objects.filter(is_published=True)[:4]
        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if markdown:
            context['content_html'] = markdown.markdown(
                self.object.content,
                extensions=['fenced_code', 'codehilite', 'tables', 'toc']
            )
        else:
            context['content_html'] = f"<p>{self.object.content}</p>"
            
        context['approved_comments'] = self.object.comments.filter(is_approved=True)
        context['related_posts'] = Blog.objects.filter(
            category=self.object.category, is_published=True
        ).exclude(id=self.object.id)[:3]
        return context

def add_comment(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug, is_published=True)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment_text')

        if name and email and comment_text:
            Comment.objects.create(
                blog=blog,
                name=name,
                email=email,
                comment_text=comment_text,
                is_approved=True
            )
            messages.success(request, 'Your comment has been submitted successfully!')
        else:
            messages.error(request, 'Please fill in all required fields.')
            
    return redirect('blog_detail', slug=slug)
