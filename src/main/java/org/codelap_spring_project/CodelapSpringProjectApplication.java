package org.codelap_spring_project;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Profile;

@SpringBootApplication(scanBasePackages = "org.codelap_spring_project.controller")
public class CodelapSpringProjectApplication {

    public static void main(String[] args) {
        SpringApplication.run(CodelapSpringProjectApplication.class, args);
    }

}
