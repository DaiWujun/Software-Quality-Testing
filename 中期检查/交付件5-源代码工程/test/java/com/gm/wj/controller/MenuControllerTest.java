package com.gm.wj.controller;

import com.gm.wj.service.AdminMenuService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Collections;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@WebMvcTest(MenuController.class)
public class MenuControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AdminMenuService adminMenuService;

    @Test
    public void testMenu() throws Exception {
        Mockito.when(adminMenuService.getMenusByCurrentUser()).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/menu"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    @Test
    public void testListAllMenus() throws Exception {
        Mockito.when(adminMenuService.getMenusByRoleId(1)).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/admin/role/menu"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }
}
