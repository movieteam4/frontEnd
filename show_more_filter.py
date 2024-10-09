def filter_show(horrors_list,story_rich_list,animation_list):
    from django.templatetags.static import static
    from django.urls import reverse
    import pandas as pd
    genre_list=['horror','story_rich','animation']
    res=''
    form_action_url = reverse('product_details')
    for n,i in enumerate([horrors_list,story_rich_list,animation_list]):
        for i2 in range(len(i)):
            img=i['宣傳照'].iloc[i2]
            ch_name=i['中文片名'].iloc[i2]
            eng_name=i['英文片名'].iloc[i2]
            if pd.isna(img) or img == '':
                img=static('dog.jpg')
            res+=f'''<div class="col-lg-3 col-md-6 align-self-center mb-30 trending-items col-md-6 {genre_list[n]}">
          <div class="item">
            <div class="thumb">
              <a href="{form_action_url}"><img src="{img}" alt="" width='261px' height='392px' ></a>
            </div>
            <div class="down-content">
              <span class="category">Action</span>
              <h4>{ch_name}</h4>
              <h4>{eng_name}</h4>
              <a href="{form_action_url}"><i class="fa fa-shopping-bag"></i></a>
            </div>
          </div>
        </div>
        '''
    return res