((arguments) => {
    let items = Array.from(document.querySelectorAll(arguments[0]));
    let reduceNULL = v => {
        try {
            if (v) {
                return v.innerText
            } else {
                return 'N/A'
            }
        } catch (e) {
            console.error(e)
            return 'N/A'
        }
    }

    let reduceTags = v => {
        try {
            if (v) {
                return Array.from(v).filter(tag=>tag.innerText).map(tag => tag.innerText).join('、').replace('\n', '、')
            } else {
                return 'N/A'
            }
        } catch (e) {
            console.error(e)
            return 'N/A'
        }
    }

    return items.map((item) => {
        console.log('handling: ', item)
        return {
            item_description: reduceNULL(item.querySelector(arguments[1])),
            item_price: reduceNULL(item.querySelector(arguments[2])),
            item_price_notes: reduceNULL(item.querySelector(arguments[3])),
            comment_count: reduceNULL(item.querySelector(arguments[4])),
            store_name: reduceNULL(item.querySelector(arguments[5])),
            product_tags: reduceTags(item.querySelectorAll(arguments[6]))
        };
    });
})([
        '*#J_goodsList > ul > li',
        'div > div:nth-child(3) > a > em',
        'div > div:nth-child(2) > strong',
        'div.p-price > strong + span',
        'div > div:nth-child(4) > strong > a',
        'div > div:nth-child(5) > span > a',
        'div > div:nth-child(6)'
    ]
)
/*
 * @Author: Flandre Scarlet i@flandrescarlet.cn
 * @Date: 2024-11-25 00:45:06
 * @LastEditors: Flandre Scarlet i@flandrescarlet.cn
 * @LastEditTime: 2024-11-25 10:18:54
 * @FilePath: /jd_spider/js/get_items_data.js
 * Copyright (c) 2024 by Flandre Scarlet, All Rights Reserved.
 * Powered by Whiterabsk
 */
