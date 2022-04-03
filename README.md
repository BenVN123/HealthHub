# Health Hub

Our hackaton project is a deep learning detection algorithm that can identify brain tumors in patient x-rays. This project uses `Python`, `HTML5`, `CSS`, `Flask`, and `Tensorflow`. In addition to the deep learning feature, the website also includes an anonymous Q&A session to talk to others about brain cancer and a list of brain tumor symptoms.

-------------------------------------------
## Inspiration
Our inspiration came from the theme, but really from how people can feel helpless when they can be taking action. People often feel like they don't know what to do if they are **diagnosed** with a brain tumor, but luckily we are here to help connect you with a local brain doctor. Our passion for implementing software into everyday uses drove us to create this end piece.

## What it does
You can upload scans of your brain, and it will determine using Artificial Intelligence if you have a tumor or not. Depending on that information, you can choose to talk to a brain doctor in your zip code area.

## How we built it
First, we used `Flask` to communicate with a backend. Using `HTML5` and `CSS` as our front end, we were able to make the website very accessible and using `Python` associated through `Flask`, we were able to create a Deep Learning Model that the user can interact with.

## Challenges we ran into
- Getting the model to be accurate. But we tried to use as many data sets as possible to make the images vague, helping the user.
- Deploying our website. We are unable to use `Heroku` because our files are too large, and it is hard to find another server to use that is free.

## Accomplishments that we're proud of
- The ability to connect people to local brain doctors. We think that this is very helpful because people need the opportunity to have a verified doctor on call.
- The ability for people to ask questions anonymously. We feel like, without this, people wouldn't feel confident in asking questions, and can help people get answers that they are desperate to find.

## What's next for Health Hub
- One thing would be moving this website interface/software to an iPhone application or Desktop app.
- Another thing would be able to connect people directly and live to a doctor.

----------------------
# Usage (Git Bash)

Install all dependencies needed for this program:
```
pip install -r requirements.txt
```

Set the Flask variable accordingly:
```
export FLASK_APP=run
```

Do the following to start the Flask application on [localhost](http://127.0.0.1:5000):
```
flask run
```


Created by [Ben Nguyen](https://github.com/BenVN123), [Rishit Agrawal](https://github.com/RishitAgrawal06), [Adarsh Agrahara](https://github.com/boogeyman-is-back-at-crabfest), and [Eshaan Kaipa](https://github.com/epicesh)
