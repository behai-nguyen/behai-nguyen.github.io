---
layout: post
title: "Python: A simple web API to search for Australian postcodes based on locality aka suburb."
description: Using the Flask-RESTX library to implement a simple web API to search for Australian postcodes based on locality aka suburb.
tags:
- Flask-RESTX
- Australian
- Postcode
- API
---

<em>Using the Flask-RESTX library to implement a simple web API to search for Australian postcodes based on locality aka suburb.</em>

| ![066-feature-image.png](https://behainguyen.files.wordpress.com/2023/05/066-feature-image.png) |
|:--:|
| *Python: A simple web API to search for Australian postcodes based on locality aka suburb.* |

🚀 Full source code and documentation: 
<a href="https://github.com/behai-nguyen/bh_aust_postcode" title="https://github.com/behai-nguyen/bh_aust_postcode" target="_blank">https://github.com/behai-nguyen/bh_aust_postcode</a>

The web service also implements a CLI which downloads Australian postcodes 
in JSON format, then extracts locality, state and postcode fields and stores
them in a SQLite database file. 

There are just a bit more than 18,500 (eighteen thousand five hundred) postcodes.
At runtime, they are loaded once into a list property of a singleton 
class instance. Searches are carried out using this list, that is in memory 
only.

Searches are always partial: i.e. any locality contains the incoming search
text is considered a match. For example, if the incoming search text is 
<code>spring</code>, then <code>Springfield</code> is a match.

The web API returns the search result as a JSON object. 

On successful:

```javascript
	{
		"status": {
			"code": 200,
			"text": ""
		},
		"data": {
			"localities": [
				{
					"locality": "ALICE SPRINGS",
					"state": "NT",
					"postcode": "0870"
				},
				...
			{
					"locality": "WILLOW SPRINGS",
					"state": "SA",
					"postcode": "5434"
				}
			]
		}
	}
```

Nothing found:

```javascript
	{
		"status": {
			"code": 404,
			"text": "No localities matched 'xyz'"
		}
	}
```

Invalid searches:

```javascript
	{
		"status": {
			"code": 400,
			"text": "'%^& Spring' is invalid. Accept only letters, space, hyphen and single quote characters."
		}
	}

	{
		"status": {
			"code": 400,
			"text": "Must have at least 3 characters: 'Sp'"
		}
	}
```

In general <code>['status']['code']</code> other than <code>HTTPStatus.OK.value</code> 
signifies search does not return any localities. Always check for 
<code>['status']['code']</code> of <code>HTTPStatus.OK.value</code> before
proceeding any further with the result.

🚀 <a href="https://github.com/behai-nguyen/bh_aust_postcode/blob/main/README.md" title="GitHub Read Me" target="_blank">GitHub Read Me</a>
should have all necessary documentation on how to get this project to run on your development server, I have tested for both Windows 10 and Ubuntu 22.10.

My other post 
on 
<a href="https://flask-restx.readthedocs.io/en/latest/index.html" title="Flask-RESTX" target="_blank">Flask-RESTX</a> -- 
<a href="https://behainguyen.wordpress.com/2022/07/12/python-flask-restx-and-the-swagger-ui-automatic-documentation/"
title="Python: Flask-RESTX and the Swagger UI automatic documentation." target="_blank">Python: Flask-RESTX and the Swagger UI automatic documentation.</a>

Thank you for reading. I do hope someone will find this project useful. Stay safe as always.

✿✿✿

Feature image sources:

<ul>
<li>
<a href="https://in.pinterest.com/pin/337277459600111737/" target="_blank">https://in.pinterest.com/pin/337277459600111737/</a>
</li>
<li>
<a href="https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper" target="_blank">https://www.omgubuntu.co.uk/2022/09/ubuntu-2210-kinetic-kudu-default-wallpaper</a>
</li>
<li>
<a href="https://seeklogo.com/vector-logo/332789/python" target="_blank">https://seeklogo.com/vector-logo/332789/python</a>
</li>
<li>
<a href="https://flask-restx.readthedocs.io/en/latest/" target="_blank">https://flask-restx.readthedocs.io/en/latest/</a>
</li>
<li>
<a href="https://www.vectorstock.com/royalty-free-vector/australia-map-with-flag-blue-red-background-vector-25323215" target="_blank">https://www.vectorstock.com/royalty-free-vector/australia-map-with-flag-blue-red-background-vector-25323215</a>
</li>
<li>
<a href="https://logos-world.net/australia-post-logo/" target="_blank">https://logos-world.net/australia-post-logo/</a>
</li>
</ul>
