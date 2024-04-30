# Who is Waldo?

*We've all played "Where's Waldo?" but today we'll play "Who's Waldo?"*

The task is a special case of membership inference, where each user has 20 images and user-level membership is to be determined. All images available are exact, and 
a user's presence in training implies all 20 of its images were used. The model is intentionally trained for a lot of epochs to induce overfitting, making it easy
to identify members.

Apart from min(loss per user) is used, any other way of aggregation fails to identify even one user (when taking top-10 ranked by score).
Gradient norm does not help either.
