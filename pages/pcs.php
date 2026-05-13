<?

$res = q("SELECT * FROM portatili ORDER BY NumPortatile;");

if ($res->num_rows) { ?>
    <div class=pcgrid>
        <? while ($row = $res->fetch_assoc()) { ?>
            nav(pc&number=pecho($row['NumPortatile']), <div class=pcbox>
                <div class="pcbox pcnum">
                    pecho($row["NumPortatile"])
                </div>
                pecho($row["Modello"])
                <hr>
                <div class=pcnote>
                    pecho($row["Note"])
                </div>
            </div>)
        <?}?>
    </div>
<?} else {?>
    <div class=pcbox>
        <div class="pcbox pcnum"> - </div> --- <hr> Niente da vedere... 
    </div>
<?}?>