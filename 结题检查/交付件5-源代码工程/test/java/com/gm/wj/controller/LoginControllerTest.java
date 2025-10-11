package com.gm.wj.controller;

import com.gm.wj.entity.User;
import com.gm.wj.service.UserService;
import org.apache.shiro.authc.IncorrectCredentialsException;
import org.apache.shiro.authc.UnknownAccountException;
import org.apache.shiro.subject.Subject;
import org.apache.shiro.util.ThreadContext;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * 针对 LoginController 的黑盒+白盒单元测试
 */
@RunWith(SpringRunner.class)
@WebMvcTest(LoginController.class)
public class LoginControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    /**
     * 批量测试 LoginController 所有接口，并输出每个接口测试结果
     */
    @Test
    public void testAllEndpoints() throws Exception {
        System.out.println("开始批量测试 LoginController 所有接口...");

        loginSuccessTest();
        System.out.println("loginSuccessTest 通过");

        loginDisabledUserTest();
        System.out.println("loginDisabledUserTest 通过");

        loginIncorrectPasswordTest();
        System.out.println("loginIncorrectPasswordTest 通过");

        loginUnknownAccountTest();
        System.out.println("loginUnknownAccountTest 通过");

        registerEmptyTest();
        System.out.println("registerEmptyTest 通过");

        registerSuccessTest();
        System.out.println("registerSuccessTest 通过");

        registerUserExistsTest();
        System.out.println("registerUserExistsTest 通过");

        registerUnknownErrorTest();
        System.out.println("registerUnknownErrorTest 通过");

        logoutTest();
        System.out.println("logoutTest 通过");

        authenticationTest();
        System.out.println("authenticationTest 通过");

        System.out.println("所有接口测试完成。覆盖率请用 Jacoco 或 IDEA 查看详细报告。");
    }

    /**
     * 测试登录接口：正常登录（用户启用）
     */
    @Test
    public void loginSuccessTest() throws Exception {
        Subject subject = mock(Subject.class);
        doNothing().when(subject).login(any());
        ThreadContext.bind(subject);

        User user = new User();
        user.setUsername("admin");
        user.setPassword("123");
        user.setEnabled(true);

        when(userService.findByUsername("admin")).thenReturn(user);

        String json = "{\"username\":\"admin\",\"password\":\"123\"}";

        mockMvc.perform(post("/api/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").exists())
                .andExpect(jsonPath("$.message").value("成功"));

        ThreadContext.unbindSubject();
    }

    /**
     * 测试登录接口：用户被禁用
     */
    @Test
    public void loginDisabledUserTest() throws Exception {
        Subject subject = mock(Subject.class);
        doNothing().when(subject).login(any());
        ThreadContext.bind(subject);

        User user = new User();
        user.setUsername("admin");
        user.setPassword("123");
        user.setEnabled(false);

        when(userService.findByUsername("admin")).thenReturn(user);

        String json = "{\"username\":\"admin\",\"password\":\"123\"}";

        mockMvc.perform(post("/api/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("该用户已被禁用"));

        ThreadContext.unbindSubject();
    }

    /**
     * 测试登录接口：密码错误
     */
    @Test
    public void loginIncorrectPasswordTest() throws Exception {
        Subject subject = mock(Subject.class);
        doThrow(new IncorrectCredentialsException()).when(subject).login(any());
        ThreadContext.bind(subject);

        String json = "{\"username\":\"admin\",\"password\":\"wrongpass\"}";

        mockMvc.perform(post("/api/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("密码错误"));

        ThreadContext.unbindSubject();
    }

    /**
     * 测试登录接口：账号不存在
     */
    @Test
    public void loginUnknownAccountTest() throws Exception {
        Subject subject = mock(Subject.class);
        doThrow(new UnknownAccountException()).when(subject).login(any());
        ThreadContext.bind(subject);

        String json = "{\"username\":\"nouser\",\"password\":\"123\"}";

        mockMvc.perform(post("/api/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("账号不存在"));

        ThreadContext.unbindSubject();
    }

    /**
     * 测试注册接口：用户名和密码不能为空
     */
    @Test
    public void registerEmptyTest() throws Exception {
        when(userService.register(any(User.class))).thenReturn(0);

        String json = "{\"username\":\"\",\"password\":\"\"}";

        mockMvc.perform(post("/api/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("用户名和密码不能为空"));
    }

    /**
     * 测试注册接口：注册成功
     */
    @Test
    public void registerSuccessTest() throws Exception {
        when(userService.register(any(User.class))).thenReturn(1);

        String json = "{\"username\":\"newuser\",\"password\":\"newpass\"}";

        mockMvc.perform(post("/api/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("注册成功"));
    }

    /**
     * 测试注册接口：用户已存在
     */
    @Test
    public void registerUserExistsTest() throws Exception {
        when(userService.register(any(User.class))).thenReturn(2);

        String json = "{\"username\":\"existuser\",\"password\":\"pass\"}";

        mockMvc.perform(post("/api/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("用户已存在"));
    }

    /**
     * 测试注册接口：未知错误
     */
    @Test
    public void registerUnknownErrorTest() throws Exception {
        when(userService.register(any(User.class))).thenReturn(99);

        String json = "{\"username\":\"erroruser\",\"password\":\"pass\"}";

        mockMvc.perform(post("/api/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("未知错误"));
    }

    /**
     * 测试登出接口
     */
    /**
     * 测试登出接口：先模拟登录，再登出
     */
    @Test
    public void logoutTest() throws Exception {
        // 模拟登录，绑定 Subject
        Subject subject = mock(Subject.class);
        doNothing().when(subject).logout();
        ThreadContext.bind(subject);

        mockMvc.perform(get("/api/logout"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("成功登出"));

        // 解绑 Subject，防止影响其他测试
        ThreadContext.unbindSubject();
    }

    /**
     * 测试身份认证接口
     */
    @Test
    public void authenticationTest() throws Exception {
        mockMvc.perform(get("/api/authentication"))
                .andExpect(status().isOk())
                .andExpect(content().string("身份认证成功"));
    }
}
