package com.gm.wj.controller;

import com.gm.wj.entity.JotterArticle;
import com.gm.wj.service.JotterArticleService;
import com.gm.wj.util.MyPage;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@WebMvcTest(JotterController.class)
public class JotterControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private JotterArticleService jotterArticleService;

    @Test
    public void saveArticleTest() throws Exception {
        Mockito.doNothing().when(jotterArticleService).addOrUpdate(any(JotterArticle.class));
        String json = "{\"id\":10086,\"articleTitle\":\"test\",\"articleAbstract\":\"content\"}";
        mockMvc.perform(post("/api/admin/content/article")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("保存成功"));
    }

    @Test
    public void listArticlesTest() throws Exception {
        MyPage<JotterArticle> myPage = new MyPage<>(); // 根据你的MyPage构造方法初始化
        Mockito.when(jotterArticleService.list(eq(0), eq(10))).thenReturn(myPage);
        mockMvc.perform(get("/api/article/10/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").exists());
    }

    @Test
    public void getOneArticleTest() throws Exception {
        JotterArticle article = new JotterArticle();
        article.setId(1); // 如果没有setTitle方法，只设置id
        Mockito.when(jotterArticleService.findById(1)).thenReturn(article);
        mockMvc.perform(get("/api/article/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result.id").value(1));
    }

    @Test
    public void deleteArticleTest() throws Exception {
        Mockito.doNothing().when(jotterArticleService).delete(1);
        mockMvc.perform(delete("/api/admin/content/article/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("删除成功"));
    }
}
