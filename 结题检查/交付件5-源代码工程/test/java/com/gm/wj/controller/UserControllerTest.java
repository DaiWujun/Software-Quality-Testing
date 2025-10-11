package com.gm.wj.controller;

import com.gm.wj.entity.User;
import com.gm.wj.service.AdminUserRoleService;
import com.gm.wj.service.UserService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Collections;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@WebMvcTest(UserController.class)
public class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;
    @MockBean
    private AdminUserRoleService adminUserRoleService;

    @Test
    public void testListUsers() throws Exception {
        Mockito.when(userService.list()).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/admin/user"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    @Test
    public void testUpdateUserStatus() throws Exception {
        Mockito.doNothing().when(userService).updateUserStatus(any(User.class));
        String json = "{\"id\":10086,\"username\":\"test\"}";
        mockMvc.perform(put("/api/admin/user/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("用户状态更新成功"));
    }

    @Test
    public void testResetPassword() throws Exception {
        User mockUser = new User();
        mockUser.setId(10086);
        mockUser.setUsername("test");
        Mockito.when(userService.resetPassword(any(User.class))).thenReturn(mockUser);
        String json = "{\"id\":10086,\"username\":\"test\"}";
        mockMvc.perform(put("/api/admin/user/password")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("重置密码成功"));
    }

    @Test
    public void testEditUser() throws Exception {
        Mockito.doNothing().when(userService).editUser(any(User.class));
        String json = "{\"id\":10086,\"username\":\"test\"}";
        mockMvc.perform(put("/api/admin/user")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("修改用户信息成功"));
    }
}
