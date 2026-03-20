
from typing import List 
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res= authorized_client.get("/posts/") 
    
    def validate(post):
        return schemas.PostOut(**post)
    post_map= map(validate, res.json())
    post_list=list(post_map)
    
    assert len(res.json())==len(test_posts)
    assert res.status_code==200 
    

# test only the authorized users can access the posts 
def test_unauthorized_user_get_all_posts(client, test_posts):
    res= client.get('/posts/')
    assert res.status_code==401


# test only the authorized users can access one post
def test_unauthorized_user_get_one_posts(client, test_posts):
    res= client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code==401
    
def test_get_one_post_not_exits(authorized_client, test_posts):
    res= authorized_client.get("/posts/8878")
    assert res.status_code==404
    
def test_get_one_post(authorized_client, test_posts):
    res= authorized_client.get(f"/posts/{test_posts[0].id}")
    posts = schemas.PostOut(**res.json())
     
    assert posts.Post.id==test_posts[0].id
    assert posts.Post.title==test_posts[0].title
    assert posts.Post.content==test_posts[0].content 
    