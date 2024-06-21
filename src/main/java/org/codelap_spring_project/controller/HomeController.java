package org.codelap_spring_project.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.CacheControl;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;


@Controller
@RequiredArgsConstructor
@Configuration
public class HomeController  implements WebMvcConfigurer {

    @RequestMapping("/")
    @CrossOrigin(origins = { "${cors.allowed-origins}" } ,methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT})
    public String home() {
        return "redirect:/boarder";
    }


    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:3001") // React 애플리케이션의 주소
                .allowedMethods("GET", "POST", "PUT", "DELETE");
    }
    @Override
//    @RequestMapping("/uploads")
    public void addResourceHandlers(ResourceHandlerRegistry registry){
        Path currentPath = Paths.get("");
        String currentDirectory = currentPath.toAbsolutePath().toString()+"/uploads/";
        System.out.println("현재 작업 디렉토리:::::::: " + currentDirectory);

        registry.addResourceHandler("/uploads/**")
                .addResourceLocations("file:" + currentDirectory)
                .setCacheControl(CacheControl.maxAge(1, TimeUnit.HOURS).cachePublic()); // 캐시 설정


    }
}