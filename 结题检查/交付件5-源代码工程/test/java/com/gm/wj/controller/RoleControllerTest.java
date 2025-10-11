package com.gm.wj.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.gm.wj.entity.*;
import com.gm.wj.service.*;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import java.util.*;

import static org.mockito.ArgumentMatchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@WebMvcTest(RoleController.class)
public class RoleControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AdminRoleService adminRoleService;
    @MockBean
    private AdminPermissionService adminPermissionService;
    @MockBean
    private AdminRolePermissionService adminRolePermissionService;
    @MockBean
    private AdminRoleMenuService adminRoleMenuService;

    @Test
    public void testListRoles() throws Exception {
        List<AdminRole> roles = Collections.singletonList(AdminRole.builder().id(1).name("admin").nameZh("管理员").enabled(true).build());
        Mockito.when(adminRoleService.listWithPermsAndMenus()).thenReturn(roles);

        mockMvc.perform(get("/api/admin/role"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result[0].name").value("admin"));
    }

    @Test
    public void testUpdateRoleStatus() throws Exception {
        AdminRole role = AdminRole.builder().id(1).name("admin").nameZh("管理员").enabled(true).build();
        Mockito.when(adminRoleService.updateRoleStatus(any(AdminRole.class))).thenReturn(role);

        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(role);

        mockMvc.perform(put("/api/admin/role/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("用户管理员状态更新成功"));
    }

    @Test
    public void testEditRole() throws Exception {
        AdminRole role = AdminRole.builder().id(1).name("admin").nameZh("管理员").enabled(true).perms(new ArrayList<>()).build();
        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(role);

        Mockito.doNothing().when(adminRoleService).addOrUpdate(any(AdminRole.class));
        Mockito.doNothing().when(adminRolePermissionService).savePermChanges(anyInt(), anyList());

        mockMvc.perform(put("/api/admin/role")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("修改角色信息成功"));
    }

    @Test
    public void testAddRole() throws Exception {
        AdminRole role = AdminRole.builder().id(2).name("user").nameZh("普通用户").enabled(true).build();
        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(role);

        Mockito.doNothing().when(adminRoleService).editRole(any(AdminRole.class));

        mockMvc.perform(post("/api/admin/role")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("修改用户成功"));
    }

    @Test
    public void testListPerms() throws Exception {
        List<AdminPermission> perms = Collections.singletonList(new AdminPermission());
        Mockito.when(adminPermissionService.list()).thenReturn(perms);

        mockMvc.perform(get("/api/admin/role/perm"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    @Test
    public void testUpdateRoleMenu() throws Exception {
        Map<String, List<Integer>> menusIds = new HashMap<>();
        menusIds.put("menusIds", Arrays.asList(1, 2, 3));
        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(menusIds);

        Mockito.doNothing().when(adminRoleMenuService).updateRoleMenu(anyInt(), anyMap());

        mockMvc.perform(put("/api/admin/role/menu")
                        .param("rid", "1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("更新成功"));
    }
}
