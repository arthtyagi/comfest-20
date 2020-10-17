/*Likes AJAX */

$(document).ready(function () {
    function updateText(btn, newCount, verb) {
        btn.text(newCount + " " + verb)
        btn.attr("data-likes", newCount)
    }
    $("#like").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var likeUrl = this_.attr("data-href")
        var likeCount = parseInt(this_.attr("data-likes")) | 0
        var addLike = likeCount + 1
        var removeLike = likeCount - 1
        if (likeUrl) {
            $.ajax({
                url: likeUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    console.log(data)
                    if (data.liked) {
                        updateText(this_, addLike, "Likes")
                    } else {
                        updateText(this_, removeLike, "Likes")
                    }

                }, error: function (error) {
                    console.log(error)
                    console.log("error")
                }
            })
        }

    })
})

/* Follower AJAX */

$(document).ready(function () {
    function updateText(btn, newCount, verb) {
        btn.text(newCount + " " + verb)
        btn.attr("data-followers", newCount)
    }
    $("#follow").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var followUrl = this_.attr("data-href")
        var followCount = parseInt(this_.attr("data-followers")) | 0
        var addFollower = followCount + 1
        var removeFollower = followCount - 1
        if (followUrl) {
            $.ajax({
                url: followUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    console.log(data)
                    if (data.liked) {
                        updateText(this_, addFollower, "Followers")
                    } else {
                        updateText(this_, removeFollower, "Followers")
                    }

                }, error: function (error) {
                    console.log(error)
                    console.log("error")
                }
            })
        }

    })
})

