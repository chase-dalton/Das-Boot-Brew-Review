SELECT re.id, r.name, r.og, r.fg, r.ibu, r.color, r.brewmethod
FROM (SELECT r3.beerid, REPLACE(r3.name, '(clone', '') AS name, r3.og, r3.fg, r3.ibu, r3.color, r3.brewmethod
        FROM (SELECT r2.beerid, REPLACE(r2.name, 'clone)', '') AS name, r2.og, r2.fg, r2.ibu, r2.color, r2.brewmethod
                FROM (SELECT r1.beerid, REPLACE(r1.name, 'clone', '') AS name, r1.og, r1.fg, r1.ibu, r1.color, r1.brewmethod
                        FROM (SELECT r0.beerid, REPLACE(r0.name, 'Clone', '') AS name, r0.og, r0.fg, r0.ibu, r0.color, r0.brewmethod
                                FROM recipes r0) r1) r2) r3) r
INNER JOIN reviews re
        ON (r.name = re.beer_name) 
WHERE r.og <= 5
AND r.fg <= 5
AND r.ibu <= 125;