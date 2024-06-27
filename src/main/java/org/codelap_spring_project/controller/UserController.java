package org.codelap_spring_project.controller;

import jakarta.validation.Valid;
import org.codelap_spring_project.domain.BoaderInsert;
import org.codelap_spring_project.domain.UserInfo;
import org.codelap_spring_project.repository.mybatis.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;


@RestController // json 파일로 배포하는 컨트롤러
@CrossOrigin(origins={ "${cors.allowed-origins}" }, allowCredentials = "true", methods = {RequestMethod.GET, RequestMethod.PUT, RequestMethod.POST})
@RequestMapping("/user")
public class UserController {
    private final UserMapper userMapper;
    @Autowired
    public UserController(UserMapper userMapper){this.userMapper = userMapper;}
    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @PostMapping(value = "/svlogin")
    public ResponseEntity<?> userLogin(@RequestBody UserInfo userInfo){
//        userMapper.toString();
        String id = userInfo.getId();
        String pass = userInfo.getPassword();

        userInfo = userMapper.checkedUser(userInfo);
        if(userInfo == null){
            System.out.println("hello");

            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("로그인 실패: ");
        }else {
            String token = jwtTokenProvider.generateToken(userInfo);
//            System.out.println(":::::::::결과"+jwtTokenProvider.validateToken(token));
            return ResponseEntity.ok(token);
        }
    }

    @PostMapping("/signup" )
    public String signup(@Valid @RequestBody UserInfo user) throws IOException, SQLException {

        System.out.println(user.getLocationx()+user.getId()+user.getGender()+user.getTagfamily()+user.getTaglike());

        Boolean result = userMapper.signup(user);
        System.out.println("::결과::"+result);

        return null;
    }
}
