package com.gm.wj.controller;

import com.gm.wj.entity.Book;
import com.gm.wj.service.BookService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Collections;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * 针对 LibraryController 的单元测试
 */
@RunWith(SpringRunner.class)
@WebMvcTest(LibraryController.class)
public class LibraryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private BookService bookService;

    /**
     * 测试获取全部书籍接口
     */
    @Test
    public void listBooksTest() throws Exception {
        Mockito.when(bookService.list()).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/books"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    /**
     * 测试新增或更新书籍接口
     */
    @Test
    public void addOrUpdateBooksTest() throws Exception {
        Mockito.doNothing().when(bookService).addOrUpdate(any(Book.class));
        String json = "{\"id\":10086,\"title\":\"Java\",\"author\":\"Tom\"}";
        mockMvc.perform(post("/api/admin/content/books")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("修改成功"));
    }

    /**
     * 测试删除书籍接口
     */
    @Test
    public void deleteBookTest() throws Exception {
        Mockito.doNothing().when(bookService).deleteById(eq(1));
        String json = "{\"id\":1,\"title\":\"Java\"}";
        mockMvc.perform(post("/api/admin/content/books/delete")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").value("删除成功"));
    }

    /**
     * 测试搜索接口：关键词为空
     */
    @Test
    public void searchResultEmptyTest() throws Exception {
        Mockito.when(bookService.list()).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/search?keywords="))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    /**
     * 测试搜索接口：有关键词
     */
    @Test
    public void searchResultWithKeywordTest() throws Exception {
        Mockito.when(bookService.Search(eq("Java"))).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/search?keywords=Java"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    /**
     * 测试按分类获取书籍接口：cid不为0
     */
    @Test
    public void listByCategoryTest() throws Exception {
        Mockito.when(bookService.listByCategory(eq(2))).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/categories/2/books"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    /**
     * 测试按分类获取书籍接口：cid为0
     */
    @Test
    public void listByCategoryZeroTest() throws Exception {
        Mockito.when(bookService.list()).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/categories/0/books"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.result").isArray());
    }

    /**
     * 测试封面上传接口
     */
    @Test
    public void coversUploadTest() throws Exception {
        MockMultipartFile file = new MockMultipartFile("file", "cover.jpg", MediaType.IMAGE_JPEG_VALUE, "test".getBytes());
        mockMvc.perform(multipart("/api/admin/content/books/covers").file(file))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("http://localhost:8443/api/file/")));
    }
}
