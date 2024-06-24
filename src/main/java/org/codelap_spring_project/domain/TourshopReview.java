package org.codelap_spring_project.domain;

import java.util.List;

public class TourshopReview {

    private String reviewId;
    private String shopId;
    private String content;
    private String author;
    private String create_at;
    private String parent_comment_id;

    private List<TourshopReview> children;

    public TourshopReview(){}

    public TourshopReview(List<TourshopReview> children, String reviewId, String shopId, String content, String author, String create_at, String parent_comment_id) {
        this.reviewId = reviewId;
        this.shopId = shopId;
        this.content = content;
        this.author = author;
        this.create_at = create_at;
        this.parent_comment_id = parent_comment_id;
        this.children = children;
    }

    public List<TourshopReview> getChildren() {
        return children;
    }

    public void setChildren(List<TourshopReview> children) {
        this.children = children;
    }

    public String getReviewId() {
        return reviewId;
    }

    public void setReviewId(String reviewId) {
        this.reviewId = reviewId;
    }

    public String getShopId() {
        return shopId;
    }

    public void setShopId(String shopId) {
        this.shopId = shopId;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getCreate_at() {
        return create_at;
    }

    public void setCreate_at(String create_at) {
        this.create_at = create_at;
    }

    public String getParent_comment_id() {
        return parent_comment_id;
    }

    public void setParent_comment_id(String parent_comment_id) {
        this.parent_comment_id = parent_comment_id;
    }
}
