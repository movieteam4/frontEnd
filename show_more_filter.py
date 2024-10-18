def filter_show(final_data,horrors_list,story_rich_list,animation_list,action_list,documentary_list,musical_list,romance_list,my_favorite,Favorite_movies_list=[],mail=False):
    from django.templatetags.static import static
    from django.urls import reverse
    import pandas as pd
    genre_list=['all','horror','story_rich','animation','action','documentary','musical','romance','my_favorite']
    res=''
    form_action_url = reverse('product_details')
    alert=''
    if mail==False:
        alert='''onclick="alert('請先登入！'); return false"'''
    for n,i in enumerate([final_data,horrors_list,story_rich_list,animation_list,action_list,documentary_list,musical_list,romance_list,my_favorite]):
        che=[]
        for N,i2 in enumerate(range(len(i))):
            img=i['宣傳照'].iloc[i2]
            ch_name=i['中文片名'].iloc[i2]
            check=''
            if ch_name in Favorite_movies_list:
                check='checked'
            if ch_name in che:
                continue
            che.append(ch_name)
            eng_name=i['英文片名'].iloc[i2]
            genre=i['類型'].iloc[i2]
            if pd.isna(img) or img == '':
                img='https://raw.githubusercontent.com/movieteam4/img/refs/heads/main/dog.jpg'
            res+=f'''<div class="col-lg-3 col-md-6 align-self-center mb-30 trending-items col-md-6 {genre_list[n]}">
          <div class="item">
            <div class="thumb">
              <a href="{form_action_url}"><img src="{img}" alt="" width='261px' height='392px' ></a>
            </div>
            <div class="down-content">
              <span class="category">{genre}</span>
              <h4>{ch_name}</h4>
              <h6>{eng_name}</h6>
              <a href="/Taiwan_movies_all/shop/?m={ch_name}"><i class="fas fa-arrow-right"></i></a>
              <div class="heart-checkbox">
                <input type="checkbox" id="heart-checkbox{N}" data-movie-title="{ch_name}" {check} />
                <label for="heart-checkbox{N}" {alert} >
                  <i class="far fa-heart" id="img_heart"></i>  <!-- 空心愛心 -->
                  <i class="fas fa-heart"></i>  <!-- 實心愛心 -->
                </label>
              </div>
            </div>

          </div>
        </div>
        '''
    return res