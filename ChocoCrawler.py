import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from toollib import autodriver
import markdownify
from bs4 import BeautifulSoup
import os
import requests

def filename_filter(filename):  
    string1="\/:*?\"<>|"
    for s1 in string1:
        filename= filename.replace(s1," ")
    return(filename)

if __name__ == '__main__':
    # 指定chromedriver.exe路径
    driver_path = "chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=Service(driver_path),options=chrome_options)
    for i in range(15079, 20000):#id为文章编号 看先知平台
        try:
            id = str(i)
            url = "https://xz.aliyun.com/news/" + id
            print(url)

            driver.get(url)
            headers = {
                "Referer": "https://xz.aliyun.com/",
                #"Cookie": "customer_timezone=8; arms_uid=de74db3f-a544-4abf-9709-11b8479fbca4; cna=FDKgIX46lFYBASABAlDqT4dh; account_info_switch=close; login_aliyunid_ticket=mBZHIzsgdZq64XXWQgyKFeuf0vpmV*s*CT58JlM_1t$w3AC$WOXI4tViI*9_87vjMLTWF*HtHfFI1p9puQFfgaJ_gPpof_BNTwUhTOoNC1ZBeeMfKJzxdnb95hYssNIZor6q7SCxRtgmGCbifG2Cd4aW0; login_aliyunid_csrf=_csrf_tk_1560863264167977; login_aliyunid_pk=1014399768132748; login_current_pk=1014399768132748; hssid=F1B4CD06C19CE93219151232E3AEF5A7; hsite=6; aliyun_country=CN; aliyun_site=CN; aliyun_lang=zh; tfstk=gfzIm_c9upvBvaqxA45wco6YMb35317q9QG8i7Lew23Lw4N8ZYkE4YrsPR2BTHPzwYw7QA2PtbS3V4wTQkkLU2J5PRMizvzUYuZ_KSnUF7fnwYe8FYrFbZP3t40R3Y_VuW0k5adYR4pz62cPuFWT0ZP3tC3R3t7Vua_Ul9H-e8nKXhhqBXp8e0hO1bhyp3LLe5CsIb--eeH-WAhoNY3-y8FO1bDte4n8e5CsZAH-K5AjNMM3Os4eNCgexZNICUL85XBoHWMssf4sODMxXAT8OPGIAxFLkHs_vfUa5mowai0TilyK1q_wvqF_2-ZYEi-iR7ELEcwhIhMaXyV-ecRJu5Nb9o3Tz_dmfRhSD4n6wUFs-AnzJqQvCfqTTuU3dQT-tyzqVxm1wUmrWroYDJOli53Kw8m0ztYnp7F0oouf7H3Y1uebVg8Xux_ic3OsmUhs3116q3AAfPkXIgIiPDhiOc511pEovfcs3116q3mKsXMN119Lq; login_aliyunid_pks=BG+k67ShqqisbhQyl121+tTy7utfbBknZHVZUiqweSXCvM=; login_aliyunid=CH****; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InY4MHVBcFhOZkxneGFrMVlGQi9md0E9PSIsInZhbHVlIjoiYWRwS29NOUZ3TUkzSnpINGRqWFRRU1BpUUFyeGVGSTdDU3FDSGJYUjFGZzJtOU1LYTF0bC9ibnh2eUE1dUJnNDg3dXBlbi90c2I1VWNRNWZnQllSUWRkenk4RUFidk5hV1FnYXZqaGRNVUorZExQVFJ6QUxRS2dmd0YzUGN3QWRQQVBYTncxVHpUOXFsNyt4YXNtT2VRPT0iLCJtYWMiOiJkMDg0NTMzODJjNmE4NmQ5OWNjOGU1NzcxZDcxOGU5N2QyMWY0YjgwMDliMjVlYzdmNjhlZDMzMDE3ODk0NjBjIiwidGFnIjoiIn0%3D; acw_tc=1a0c380917632664735507748e3432645ef2d7070851d01c0ac6926aaec9f9; XSRF-TOKEN=eyJpdiI6IjU4Q2tFUUtvOC9BVWtIU2dHaHA0T1E9PSIsInZhbHVlIjoiTktkeE5UTjFaemRSajVGanJIczI2OHZNUmJyMGUrMGVqcFhadEQrWHZ1T2JkdUd3MEU3VTFFVk00cGxWRDl6SVVrdUlJeGQ4eHYva3d4WUd5NFl4aE80ZDUvT3FtaGR4L0FzOFdpcGd1Qi9CUUZwbkNSWGY0QXU2RnpPU2IrREkiLCJtYWMiOiJkOTcxMDAyNGZjOTFhYzdiZmE3MWVlZTBlM2FmZGI5MDg4NmUyODhjYmQ2ODM1Zjk1ZTUzNjQ1MGRmODIwNWQ0IiwidGFnIjoiIn0%3D; plus_session=eyJpdiI6InNrVG5iM1B5RFhhbFJ5YWtHZkdzS2c9PSIsInZhbHVlIjoiVE5BcE1Ha3ZYSHp1d3loeHlPWGcyNUtGOXR3cG1wMmQ3VjB4SUJzZ29paWlwUWNEcmtMUU1wYWFwLy9rZFo3dW9BVnlZNkNndElYTXd4WEdZQURURHBuQmFHSmU2Q2VlYnJSVEtxaGRWUnVRVCs0OVl5Qmx3UTFmZTJEajUxR0giLCJtYWMiOiJlNTY3Nzk2Njk0M2VjNTg4MzNkOTRhNWI5ODc0MTAyYWVjMWFiODEyZGVkNzNlZmI2NjZjNjIwZTIzZmRjZmE1IiwidGFnIjoiIn0%3D; SERVERID=6ca2b1097a25813135a2db094b58bc2d|1763266688|1763262730; ssxmod_itna=1-YuD=q_OGCGOKG=G0idoD5Ee_DcDUED0dGMD3qiQGgDYq7=GFKDCEOKEGaegqSx4BvNDGEu01qUjqDszexiNDAxq0iDCbej4Ht_D42tzinC0vPY96700Iqg9QWvpP8n7ok9aFy/6/lqsBUpY7YYf2vtKAwKFAiPPODrDB3DbqDyz75YexGGj4GwDGoD34DiDDPLD03Db4D_7pTD7Enas=9bVneDQ4GyDitDKumbxi3DA4Dj36h45fnipDDBDGUzptHDG4Gfi1YD0kY25brYK4GW3ca3VcmGEUxHrDhbx0taDBLt0VOEusVhidHPXg1UplEzcdDCKD7w7jRbxkKARF0_TvqbP7iwBYoreRxx=DxH7xPDii7eaAqd7xi0DdBq_GreEifoQMie1ov_YkM7YAhw_ADzreYChtjWiW__io=itCiiwgY=BqrAYiB4IrAMA5VDYdYrGBwjepa=rMmx4D; ssxmod_itna2=1-YuD=q_OGCGOKG=G0idoD5Ee_DcDUED0dGMD3qiQGgDYq7=GFKDCEOKEGaegqSx4BvNDGEu01qUY4DW_SnrWhdYDjbwdP8i12_ddD05jf0n9ATBfaXCI5chFrl6rxL0VIp85LqpN/u/XGG3RQ_3CtM6f/B_XiB6R_T0xj8GXIjf5jn=L3A2=MrT2jwtruWdRDl_xdLbZm2fuIjWY4PT/t1RK_T9CkBdHELx/eeKZRnawwwnx4oXhSeHD5quNfc3KsTjoHYenKn2yGAdXPu5q5fbrPMwP93UeE3LBi6fqlI8XsMEXRIgfGB4lxKno74Wi6THhra6r7ArNYiaoWQNQH4WaKTGTw3qDezSa=DQarsGokdA3qD1lMk2LbwoH28iKLbmbiOba_2F=SWBi8U4_bTFzDi6TQPltsMrl2aVEhewEqkirmNVxKcWEqfIakO9x7F2Hv_tH0HXg=CnH_SrQSaxd1axh/brzapTQzXMkGlCGr1YDbzdH6=zFhFseFzLQvO6RZaKMjarIK9t_8b170T8bOgzQ=mK44Ne4y8THrt2ntyehlhWt4iEtvjIb56fX/WKqI_fDaTw_zQpE8MmTw/w6Cig4x_Dd=D4MB=bxhLri5vFYAzzg8WI3HYSXE5pa7UpRQbSWOMkjMK_5_ie5rZrO5ZB5DOx1GwsYZcsDMYZ4D; acw_sc__v2=197d84838-b6d9d7ce0be61d80cc98c8aa91537c3b12f60bee2c58277f68"  # 替换为实际cookie
            }

            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            
            # 尝试多种方式获取文章标题
            title_tag = soup.find('title')
            title_text = title_tag.text if title_tag else None
            
            # 也尝试从文章内容中获取标题
            article_title = soup.find('h1', class_='article-title')
            if article_title:
                title_text = article_title.text.strip()
                
            print(f"URL: {url}, Title: {title_text}")
            
            if not title_text or ('400 -' in title_text) :
                time.sleep(10)
                continue
                
            f = filename_filter(title_text)
            filename = "./xianzhi/"+id+"-"+ f + ".md"

            if not os.path.exists("./xianzhi/images"):
                os.makedirs("./xianzhi/images")
            
            # 更精确地获取文章内容，而不是整个页面
            article_content = None
            
            # 尝试常见的文章内容容器
            article_containers = [
                soup.find('div', class_='article-content'),
                soup.find('div', class_='content'),
                soup.find('article'),
                soup.find('div', id='content'),
                soup.find('div', class_='article-body')
            ]
            
            for container in article_containers:
                if container:
                    article_content = container
                    break
            
            # 如果找不到具体的文章容器，就使用整个页面
            if not article_content:
                article_content = soup.body if soup.body else soup
            
            # 提取文章内容中的图片
            article_img_tags = article_content.find_all("img")
            
            # 下载文章图片
            for img_tag in article_img_tags:
                try:
                    img_url = img_tag.get("src")
                    if img_url:
                        # 处理相对路径
                        if not img_url.startswith(('http://', 'https://')):
                            img_url = "https://xz.aliyun.com" + img_url
                        
                        img_name = os.path.basename(img_url)
                        # 添加ID前缀避免文件名冲突
                        img_name = f"{id}_{img_name}"
                        
                        img_data = requests.get(img_url, headers=headers, timeout=10).content
                        with open(f"./xianzhi/images/{img_name}", "wb") as img_file:
                            img_file.write(img_data)
                except Exception as img_e:
                    print(f"下载图片失败: {str(img_e)}")
            
            # 将文章内容转换为Markdown
            article_html = str(article_content)
            md_content = markdownify.markdownify(article_html, heading_style="ATX")
            
            # 修改Markdown中的图片引用路径
            for img_tag in article_img_tags:
                try:
                    img_url = img_tag.get("src")
                    if img_url:
                        if not img_url.startswith(('http://', 'https://')):
                            img_url = "https://xz.aliyun.com" + img_url
                        
                        original_img_name = os.path.basename(img_url)
                        new_img_name = f"{id}_{original_img_name}"
                        md_content = md_content.replace(img_url, f"images/{new_img_name}")
                except Exception as img_e:
                    print(f"修改图片路径失败: {str(img_e)}")
            
            # 添加一些元信息
            md_content = f"# {title_text}\n\n来源: {url}\n\n{md_content}"
            
            # 保存Markdown文件
            with open(filename, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)
                
            print(f"成功保存: {filename}")
        except Exception as e:
            print(str(e))
            pass
        time.sleep(5)
    driver.quit()