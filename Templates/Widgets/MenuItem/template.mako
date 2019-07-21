<%page args="menuitem"/>
$(menuitem)
<a href="#${menuitem['id']}">
    <div class="menuicon">
        <i class="${menuitem['icon']}"></i>
    </div>
    ${menuitem['name']}
</a>
