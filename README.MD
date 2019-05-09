# confessions-ios-backend

Backend Implementation for Confessions iOS App. 

iOS Code: https://github.com/lucyxubroad/confessions-ios-app

# Specified Routes

## 1. Get all posts: GET /api/posts

### Response on Success
```
{
  "success": True,
  "data": [
    {
      "id": 1, 
      "score": 0, 
      "text": "hola", 
      "comment_count": 0, 
      "username": "random", 
      "longitude": -42.453449, 
      "latitude": -76.473503
    },
    {
      "id": 2, 
      "score": 0, 
      "text": "hola", 
      "comment_count": 0, 
      "username": "random", 
      "longitude": -45.453449, 
      "latitude": -76.473503
    }
  ]
}
```

## 2. Get all posts near location: GET /api/posts/long={longitude}&lat={latitude}/

### Response on Success
```
{
  "success": True,
  "data": [
    {
      "id" 0,
      "score": 0,
      "text": "My First Post!",
      "comment_count": 0,
      "username": "Lucy",
      "longitude": <NEARBY LOCATION LONGITUDE>,
      "latitude": <NEARBY LOCATION LATITUDE>
    },
    {
      "id": 1,
      "score": 0,
      "text": "My Second Post!",
      "comment_count": 0,
      "username": "Lucy",
      "longitude": <NEARBY LOCATION LONGITUDE>,
      "latitude": <NEARBY LOCATION LATITUDE>
    }
  ]
}
```

## 3. Create a post: POST /api/posts

### Post Body
```
{
  "text": <USER INPUT>,
  "username": <USER INPUT>,
  "longitude": <USER INPUT>,
  "latitude": <USER INPUT>
}
```

### Response on Success
```
{
  "success": True,
  "data": {
    "id": <ID>
    "score": 0,
    "comment_count": 0,
    "text": <USER INPUT FOR TEXT>,
    "username": <USER INPUT FOR USERNAME>,
    "longitude": <USER INPUT FOR LONGITUDE>,
    "latitude": <USER INPUT FOR LATITUDE>
  }
}
```

## 4. Get a specific post: GET /api/post/{id}/
### Response on Success
```
{
  "success": True,
  "data": <POST WITH ID {id}>
} 
```

## 5. Get comments for post: GET /api/post/{id}/comments/
### Response on Success
```
{
  "success": True,
  "data":
    [
      {
        "id": 0,
        "score": 0,
        "text": "My First Comment!",
        "username": "Young",
      }
    ]
}
```

## 6. Post a comment: POST /api/post/{id}/comment/
### Post Body
```
{
  "text": <USER INPUT>,
  "username": <USER INPUT>,
}
```

### Response on Success
```
{
  "success": true,
  "data": {
    "id": <ID>,
    "score": 0,
    "text": <USER INPUT FOR TEXT>,
    "username": <USER INPUT FOR USERNAME>,
  }
}
```

## 7. Like a post: POST /api/post/{id}/vote/
### Post Body
```
{
  "vote": <true for like> 
}
```

### Response on Success
```
{
  "success": True,
  "data": <POST WITH ID {id} WHERE THE SCORE IS ADJUSTED ACCORDINGLY>
} 
```
## 8. Like a comment  POST /api/comment/{id}/vote/
### Post Body
```
{
  "vote": <true for like> 
}
```
### Response on Success
```
{
  "success": True,
  "data": <COMMENT WITH ID {id} WHERE THE SCORE IS ADJUSTED ACCORDINGLY>
} 
```

## 9. Register a user  POST /register/
### Post Body
```
{
  "email": "email@gmail.com",
  "password": "password"
}
```
### Response on Success
```
{
  "session_token": "WdLiluxxZVkPUHsoqnfcQ1YpARuj9Z7or3COA4HNNAv" ,
  "session_expiration": "2018-11-06 21:12:54.851118" ,
  "update_token": "7fd15938c823cf58e78019bea2af142f9449696a",
  "user_id": 0,
  "photo_id": 0
} 
```


## 10. Login a user  POST /login/
### Post Body
```
{
  "email": "email@gmail.com",
  "password": "password"
}
```
### Response on Success
```
{
  "session_token": "WdLiluxxZVkPUHsoqnfcQ1YpARuj9Z7or3COA4HNNAv" ,
  "session_expiration": "2018-11-06 21:12:54.851118" ,
  "update_token": "7fd15938c823cf58e78019bea2af142f9449696a",
  "user_id": 0,
  "photo_id": 0
} 
```

## 11. Renew user session POST /session/

### Response on Success
```
{
  "session_token": "WdLiluxxZVkPUHsoqnfcQ1YpARuj9Z7or3COA4HNNAv" ,
  "session_expiration": "2018-11-06 21:12:54.851118" ,
  "update_token": "7fd15938c823cf58e78019bea2af142f9449696a",
  "user_id": 0,
  "photo_id": 0
} 
```

### Response on Failure
```
{
  "error": "Invalid update token.'"
} 
```

## 12. Check user session GET /secret/

### Response on Success
```
{
  "message": "You have successfully implemented sessions."
} 
```

### Response on Failure
```
{
  "error": "Invalid session token.'"
} 
```




