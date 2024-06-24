package org.codelap_spring_project.controller;

import org.codelap_spring_project.domain.*;
import org.codelap_spring_project.repository.mybatis.TourShopMapper;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.util.*;

@RestController
@CrossOrigin(origins = { "${cors.allowed-origins}" },allowCredentials = "true",methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT})
@RequestMapping("/tourshop")
public class TourShopController {

    private final TourShopMapper tourShopMapper;

    @Autowired
    public TourShopController(TourShopMapper tourShopMapper) {
        this.tourShopMapper = tourShopMapper;
    }
    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @GetMapping(value = {"/svshopmain?page", "/svshopmain","/svshopmain/", "/svshopmain?user_id"})
//    public String list(Model model/*, @RequestHeader("Authorization") String token*/,@RequestParam(required = false, defaultValue = "1")String page) {
//        String userId = "admin";
    public Map<String, Object> list(Model model, @RequestHeader("Authorization") String token,@RequestParam(required = false, defaultValue = "1")String page) {
        String userId = jwtTokenProvider.getid(token);

        // 페이징 처리
        int currentPage = 1;
        if (page != null) {
//            System.out.println("page:::" +  page);
            currentPage = Integer.parseInt(page);
        }
        int totalProducts = tourShopMapper.totalPage();
//        System.out.println("totalProducts:::" + totalProducts);
        int productPerPage = 24;
        int totalPages = (int) Math.ceil((double) totalProducts / productPerPage);
//        System.out.println("totalPages:::" + totalPages);
        int startRow = (currentPage - 1) * productPerPage + 1;
        int endRow = currentPage * productPerPage;

        List<TourshopMain> tourshops = tourShopMapper.findAll(startRow, endRow);
        List<List<String>> shopList = new ArrayList<>();

        for (TourshopMain tourshop : tourshops) {
            String[] shop = new String[7];
            shop[0] = tourshop.getShopId();
            shop[1] = tourshop.getImageName();
            shop[2] = tourshop.getTourTitle();
            shop[3] = tourshop.getContent();
            shop[4] = tourshop.getTourPrice();
            shop[5] = tourshop.getLocation();
            shop[6] = tourshop.getReviews_count();
            shopList.add(Arrays.asList(shop));
        }

        System.out.println("shopList:::" + shopList);


        final int MAX_PAGE_LIMIT = 5;
        int startPage = (totalPages - currentPage) < MAX_PAGE_LIMIT ? totalPages - MAX_PAGE_LIMIT + 1 : currentPage;
        if(totalPages<MAX_PAGE_LIMIT){startPage=1;}
        int endPage = Math.min(startPage + MAX_PAGE_LIMIT -1, totalPages);

        model.addAttribute("items", tourshops);
        Map<String, Object> data = new HashMap<>();
        data.put("shop", shopList);
        data.put("currentPage", currentPage);
        data.put("endPage", endPage);
        data.put("maxPageNumber", MAX_PAGE_LIMIT);
        data.put("startPage", startPage);
        data.put("totalPage", totalPages);
        data.put("userId", userId);

        return data;
//        return "OK";
    }


    // 투어 상품 상세페이지
    @GetMapping("/svshopdetail/{id}")
    public Map<String, Object> shopDetail(@PathVariable String id) {
        String shopId = "" ;
        if(id != null){
            shopId = id;
        }
        Map<String, Object> data = new HashMap<>();
        List<Tourshop> shopResult = tourShopMapper.shopDetail(id);
        List<TourshopReview> reviewResult = tourShopMapper.shopDetailReview(id);
        List<TourshopReview> reviews = new ArrayList<>();
        Map<String, TourshopReview> reviewMap = new HashMap<>();

        for (TourshopReview row : reviewResult) {

            // 리뷰 댓글 저장하는 리스트
            String parentId = row.getParent_comment_id();

            if (parentId == null) {
                reviewMap.put(row.getReviewId(), row);
                reviews.add(row);
            } else {
                List<TourshopReview> childComment = new ArrayList<>();

                childComment.add(row);
                reviewMap.get(parentId).setChildren(childComment);
            }
        }
        System.out.println("reviews:::" + reviews);

        data.put("shop ", shopResult.get(0));
        data.put("reviews ", reviews);


        return data;
    }



    // 투어 상품 등록
//    @PostMapping("/add")
//    public String addProduct(@RequestParam("files") MultipartFile[] files,@RequestHeader("Authorization") String token, @Valid @ModelAttribute )



//    // 투어 상품 삭제
//    @GetMapping("/svshopdelete/{id}")
//    public Map<String, Boolean> shopDelete(@PathVariable String id) {
//        String shopId = id;
//        tourShopMapper.shopDeletereview(id);
//
//        boolean result = tourShopMapper.shopDelete(id);
//        Map<String, Boolean> resultMe = new HashMap<>();
//        resultMe.put("result",result);
//
//        return resultMe;
//    }

}
